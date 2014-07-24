# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Group'
        db.create_table(u'mla_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
        ))
        db.send_create_signal(u'mla', ['Group'])

        # Adding model 'Annotation'
        db.create_table(u'mla_annotation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('begin', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['mla.Group'])),
        ))
        db.send_create_signal(u'mla', ['Annotation'])

        # Adding model 'Shortcut'
        db.create_table(u'mla_shortcut', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('tooltip', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=12, blank=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal(u'mla', ['Shortcut'])


    def backwards(self, orm):
        # Deleting model 'Group'
        db.delete_table(u'mla_group')

        # Deleting model 'Annotation'
        db.delete_table(u'mla_annotation')

        # Deleting model 'Shortcut'
        db.delete_table(u'mla_shortcut')


    models = {
        u'mla.annotation': {
            'Meta': {'ordering': "('created', 'creator')", 'object_name': 'Annotation'},
            'begin': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['mla.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
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