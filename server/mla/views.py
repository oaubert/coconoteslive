from .models import Annotation, Group

import re
import datetime
import time

from django.template import RequestContext
from django.shortcuts import render_to_response

from rest_framework import generics
from .serializers import AnnotationSerializer

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
        'shortcut': shortcut
    }, context_instance=RequestContext(request))

def root(request, *p):
    return render_to_response('root.html', {
        'groups': Group.objects.all()
    })

def export_view(request, group=None, t0=None, **kw):
    def cleanup(m):
        return re.subn("[^-a-zA-Z0-9_]", "_", m.strip())[0]

    if group is None:
        qs = Annotation.objects.order_by('created')
    else:
        qs = Annotation.objects.filter(group__name=group).order_by('created')
    if not qs.count():
        return render_to_response('message.html', {
            'label': 'Error',
            'message': 'No message in group %s.' % group,
            })
    if t0 is None:
        # Use first value
        t0 = qs[0].created
    else:
        # Convert ts (in ms) to datetime
        t0 = datetime.datetime(*time.localtime(float(t0))[:7])

    # Extract custom categories
    if ':' in a.data:
        cat, data = a.data.split(":", 1)
        cat = cat.strip()
        data = data.strip()
    else:
        cat = ""
        data = a.data.strip()

    return render_to_response('message.html', {
        'label': 'Exported data',
        'message': "\n".join("%d [%s] %s" % (
            long((a.created - t0).total_seconds()),
            ",".join(cleanup(m) for m in (cat, a.category, a.creator) if m),
            (a.data.replace("\n", " ") or cleanup(a.category) or "(empty)")) for a in qs)
    })
