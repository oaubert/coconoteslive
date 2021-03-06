from .models import Annotation, Group, Shortcut

import re
import datetime
from dateutil.relativedelta import relativedelta
import time
import json
import itertools

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse

from rest_framework import generics
from .serializers import AnnotationSerializer, ShortcutSerializer, ShortcutKeySerializer

# Reaction time in seconds (substracted from annotation begin time).
REACTIONTIME = 10

class AnnotationList(generics.ListCreateAPIView):
    model = Annotation
    serializer_class = AnnotationSerializer

    def get_queryset(self):
        return self.model.objects.filter(group__name=self.kwargs['group'])

    def pre_save(self, obj):
        obj.group = Group.objects.get(name=self.kwargs['group'])
        obj.source = ",".join((self.request.META.get('REMOTE_ADDR', '?'),
                               self.request.META.get('REMOTE_HOST', '?')))

class AnnotationDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Annotation
    serializer_class = AnnotationSerializer

    def get_queryset(self):
        return self.model.objects.filter(group__name=self.kwargs['group'])

class ShortcutKeyList(generics.ListCreateAPIView):
    model = Shortcut
    serializer_class = ShortcutKeySerializer

    def get_queryset(self):
        return Shortcut.objects.values('group').annotate().order_by()

class ShortcutList(generics.ListCreateAPIView):
    model = Shortcut
    serializer_class = ShortcutSerializer

    def get_queryset(self):
        if 'block' in self.kwargs and self.kwargs['block']:
            return self.model.objects.filter(group=self.kwargs['block'])
        else:
            return self.model.objects.all()

def group_view(request, group=None, shortcut=None, **kw):
    try:
        g = Group.objects.get(name=group)
    except Group.DoesNotExist:
        return render_to_response('message.html', {
            'label': 'Error',
            'message': 'Group %s does not exist.' % group,
            })

    if not shortcut:
        shortcut = 'numaddict'

    if 'filter' in request.GET:
        filteredcss = """.topcoat-list__item.category-%s {
display: list-item;
}
.topcoat-list__item {
display: none;
}
""" % request.GET['filter']
    else:
        filteredcss = ""
    return render_to_response('client.html', {
        'filter': request.GET.get('filter', ''),
        'group': g,
        'shortcut': shortcut,
        'customcss': filteredcss + "\n" + "\n".join(".category-%(identifier)s .annotation-category, .category-button.category-%(identifier)s { background-color: %(color)s }" % s.__dict__
                                                    for s in Shortcut.objects.exclude(color="")),
        'viewonly': 'viewonly' in request.GET,
        'shortcuts': json.dumps(dict( (k, list(v)) for k, v in itertools.groupby(Shortcut.objects.order_by('group', 'position').values(), lambda x: x['group']) )),
    }, context_instance=RequestContext(request))

def root(request, *p):
    return render_to_response('root.html', {
        'groups': Group.objects.all()
    })

def sync_view(request, group=None, **kw):
    """Synchronization view.

    It can be used by recorder application to send synchronization information.
    """
    action = request.GET.get('action', 'GENERIC_ACTION')
    a = Annotation(data='%s - %s' % (action, str(time.time())),
                   creator='_admin',
                   category='admin',
                   group=Group.objects.get(name=group))
    a.begin = datetime.datetime.now()
    a.end = a.begin
    a.save()
    response = HttpResponse(content_type='text/plain; charset=utf-8')
    response.write("OK %s %s" % (action, unicode(a.created)))
    return response

def export_view(request, group=None, **kw):
    def cleanup(m):
        return re.subn("[^-a-zA-Z0-9_]", "_", m.strip())[0]

    advene = request.GET.get('advene', None)
    form = request.GET.get('format', 'text')

    if group is None:
        qs = Annotation.objects.order_by('created')
    else:
        qs = Annotation.objects.filter(group__name=group).order_by('created')
    if not qs.count():
        return render_to_response('message.html', {
            'label': 'Error',
            'message': 'No message in group %s.' % group,
            })
    absolute = request.GET.get('absolute', False)
    t0 = request.GET.get('t0', None)
    # Offset (in seconds) applied additionally to the default t0
    adjust = long(request.GET.get('adjust', 0))

    if t0 is None:
        # Use first value or first REFTIME value
        refs = qs.filter(data__contains='REFTIME')
        if refs.count():
            # REFTIME is expected to contain a timestamp in the form
            # mm:ss matching the position of the annotation in the recording.
            t0 = refs[0].created
            l = re.findall("REFTIME=([0-9]+:[0-9]+)", refs[0].data)
            if l:
                (minutes, seconds) = [ int(i) for i in l[0].split(':') ]
                t0 = t0 + relativedelta(minutes=-minutes, seconds=-seconds)
        else:
            # Fallback on first annotation
            t0 = qs[0].created
    else:
        # Convert ts (in ms) to datetime
        t0 = datetime.datetime(*time.localtime(float(t0))[:7])
        # Hackish way of specifying tzinfo
        t0 = t0.replace('tzinfo', qs[0].created.tzinfo)

    def get_begin(a):
        """Return begin time in seconds.
        """
        # Compute begin: we consider that a.created is more trusted
        # than a.end, so use it as a reference (for end time),
        # considering that transmission time is negligible.
        # We substract the annotation duration to get the annotation begin
        duration = long((a.end - a.begin).total_seconds())
        return max(0, long((a.created - t0).total_seconds()) - duration - REACTIONTIME + adjust)

    def get_end(a):
        """Return end time in seconds.
        """
        duration = long((a.end - a.begin).total_seconds())
        return get_begin(a) + max(duration, 30)

    def timerange(a):
        if absolute:
            return unicode(a.created)
        begin = get_begin(a)
        end = get_end(a)
        if advene:
            return "%d %d" % (1000 * begin, 1000 * end)
        else:
            return "%d-%d" % (begin, end)

    def isvalid(a):
        return a.created >= t0

    if form == 'json':
        response = HttpResponse(content_type='application/json')
        response.write(json.dumps([
            {    "begin": 1000 * get_begin(a),
                 "end": 1000 * get_end(a),
                 "tags": [],
                 "media": request.GET.get("media", group),
                 "content": {
                     "description": a.data.strip(),
                     "title": a.data.strip().split("\n")[0]
                },
                 "meta": {
                     "dc:contributor": a.creator,
                     "dc:created": a.created.isoformat(),
                     "dc:modified": a.created.isoformat(),
                     "dc:creator": a.creator
                 },
                 "type_title": request.GET.get("type_title", "LiveContribution"),
                 "type": request.GET.get("type", "live_contribution"),
                 "id": a.uuid
             }
            for a in qs if isvalid(a) ], indent=2))
    else:
        response = HttpResponse(content_type='text/plain; charset=utf-8')
        response.write("\n".join("%s [%s] %s" % (
            timerange(a),
            ",".join(cleanup(m) for m in (a.category, a.creator) if m),
            (a.data.strip().replace("\n", " ") or cleanup(a.category) or "(empty)")) for a in qs
                                 if isvalid(a))
                   )
    return response
