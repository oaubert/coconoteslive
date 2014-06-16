from .models import Annotation, Group

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
    return render_to_response('client.html', {
        'group': group,
        'shortcut': shortcut
    }, context_instance=RequestContext(request))

def root(request, *p):
    return render_to_response('root.html', {
        'groups': Group.objects.all()
    })
