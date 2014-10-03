from .models import Annotation, Group, Shortcut

import re
import datetime
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

    return render_to_response('client.html', {
        'group': group,
        'shortcut': shortcut,
        'customcss': "\n".join(".category-%(identifier)s .annotation-category, .category-button.category-%(identifier)s { background-color: %(color)s }" % s.__dict__
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
    response = HttpResponse(mimetype='text/plain; charset=utf-8')
    response.write("OK %s %s" % (action, unicode(a.created)))
    return response

def export_view(request, group=None, **kw):
    def cleanup(m):
        return re.subn("[^-a-zA-Z0-9_]", "_", m.strip())[0]

    advene = request.GET.get('advene', None)

    if group is None:
        qs = Annotation.objects.order_by('created')
    else:
        qs = Annotation.objects.filter(group__name=group).order_by('created')
    if not qs.count():
        return render_to_response('message.html', {
            'label': 'Error',
            'message': 'No message in group %s.' % group,
            })
    t0 = request.GET.get('t0', None)
    if t0 is None:
        # Use first value
        refs = qs.filter(data__contains='START', category='admin')
        if refs.count():
            t0 = refs[0].created
        else:
            # Fallback on first annotation
            t0 = qs[0].created
    else:
        # Convert ts (in ms) to datetime
        t0 = datetime.datetime(*time.localtime(float(t0))[:7])
        # Hackish way of specifying tzinfo
        t0 = t0.replace('tzinfo', qs[0].created.tzinfo)

    def timerange(a):
        # Compute begin: we consider that a.created is more trusted
        # than a.end, so use it as a reference (for end time),
        # considering that transmission time is negligible.
        # We substract the annotation duration to get the annotation begin
        duration = long((a.end - a.begin).total_seconds())
        begin = max(0, long((a.created - t0).total_seconds()) - duration - REACTIONTIME)
        end = begin + max(duration, 30)
        if advene:
            return "%d %d" % (1000 * begin, 1000 * end)
        else:
            return "%d-%d" % (begin, end)

    def isvalid(a):
        return a.created > t0

    response = HttpResponse(mimetype='text/plain; charset=utf-8')
    response.write("\n".join("%s [%s] %s" % (
        timerange(a),
        ",".join(cleanup(m) for m in (a.category, a.creator) if m),
        (a.data.strip().replace("\n", " ") or cleanup(a.category) or "(empty)")) for a in qs.exclude(category='admin')
                             if isvalid(a))
                   )
    return response

