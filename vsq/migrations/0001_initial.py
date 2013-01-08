# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Domanda'
        db.create_table('vsq_domanda', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
            ('testo', self.gf('django.db.models.fields.TextField')()),
            ('testo_html', self.gf('django.db.models.fields.TextField')()),
            ('approfondimento', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('approfondimento_html', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('accompagno', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('vsq', ['Domanda'])


    def backwards(self, orm):
        # Deleting model 'Domanda'
        db.delete_table('vsq_domanda')


    models = {
        'vsq.domanda': {
            'Meta': {'object_name': 'Domanda'},
            'accompagno': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'approfondimento': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'approfondimento_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'testo': ('django.db.models.fields.TextField', [], {}),
            'testo_html': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['vsq']