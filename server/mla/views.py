from rest_framework import generics
from .models import Annotation
from .serializers import AnnotationSerializer

class AnnotationList(generics.ListCreateAPIView):
    model = Annotation
    serializer_class = AnnotationSerializer

class AnnotationDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Annotation
    serializer_class = AnnotationSerializer
