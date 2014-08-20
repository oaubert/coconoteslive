# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Annotation.uuid'
        db.add_column(u'mla_annotation', 'uuid',
                      self.gf('django.db.models.fields.CharField')(default='353f8023-068e-4a95-aea1-47ba4cf566c5', unique=False, max_length=36),
                      keep_default=False)

        # Adding field 'Annotation.creatoruuid'
        db.add_column(u'mla_annotation', 'creatoruuid',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=36, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Annotation.uuid'
        db.delete_column(u'mla_annotation', 'uuid')

        # Deleting field 'Annotation.creatoruuid'
        db.delete_column(u'mla_annotation', 'creatoruuid')


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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'c0faf879-0de4-4bcb-8276-ef4eb4b05cd7'", 'unique': 'False', 'max_length': '36'})
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
