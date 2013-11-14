from rest_framework import serializers
from .models import Annotation

class AnnotationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Annotation
        fields = ('id', 'creator', 'created', 'begin', 'end', 'data', 'category')
