# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Utente'
        db.create_table('vsq_utente', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('nickname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=128, null=True, blank=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
        ))
        db.send_create_signal('vsq', ['Utente'])


    def backwards(self, orm):
        # Deleting model 'Utente'
        db.delete_table('vsq_utente')


    models = {
        'vsq.domanda': {
            'Meta': {'object_name': 'Domanda'},
            'accompagno': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'accompagno_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'approfondimento': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'approfondimento_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'}),
            'testo': ('django.db.models.fields.TextField', [], {}),
            'testo_html': ('django.db.models.fields.TextField', [], {})
        },
        'vsq.utente': {
            'Meta': {'object_name': 'Utente'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'user_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['vsq']