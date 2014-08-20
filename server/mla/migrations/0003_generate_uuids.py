# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
import uuid

def make_uuid():
    return str(uuid.uuid4())

class Migration(DataMigration):

    def forwards(self, orm):
        import random, sha, string
        for annotation in orm.Annotation.objects.all():
            annotation.uuid = make_uuid()
            annotation.creatoruuid = make_uuid()
            annotation.save()

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

    models = {
        u'mla.annotation': {
            'Meta': {'ordering': "('created', 'creator')", 'object_name': 'Annotation'},
            'begin': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'creatoruuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['mla.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'9878e952-3fd6-42f5-8d30-adc62faf3870'", 'unique': 'True', 'max_length': '36'})
        },
        u'mla.group': {
            'Meta': {'ordering': "('name', 'label')", 'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'mla.shortcut': {
            'Meta': {'ordering': "('position', 'label')", 'object_name': 'Shortcut'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'tooltip': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        }
    }

    complete_apps = ['mla']
    symmetrical = True
