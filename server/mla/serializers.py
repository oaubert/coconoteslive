from rest_framework import serializers
from .models import Annotation, Shortcut

class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ('id', 'uuid', 'creator', 'created', 'begin', 'end', 'data', 'category', 'source', 'creatoruuid')
        write_only_fields = ('creatoruuid', )

class ShortcutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shortcut
        fields = ('identifier', 'group', 'label', 'tooltip', 'color', 'position')


class ShortcutKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Shortcut
        fields = ('group', )
