from rest_framework import generics
from .models import Annotation
from .serializers import AnnotationSerializer

class AnnotationList(generics.ListCreateAPIView):
    model = Annotation
    serializer_class = AnnotationSerializer

    def pre_save(self, obj):
        obj.source = ",".join((self.request.META.get('REMOTE_ADDR', '?'),
                               self.request.META.get('REMOTE_HOST', '?')))

class AnnotationDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Annotation
    serializer_class = AnnotationSerializer
