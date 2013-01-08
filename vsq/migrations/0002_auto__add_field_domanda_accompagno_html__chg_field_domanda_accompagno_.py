# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Domanda.accompagno_html'
        db.add_column('vsq_domanda', 'accompagno_html',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'Domanda.accompagno'
        db.alter_column('vsq_domanda', 'accompagno', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Domanda.slug'
        db.alter_column('vsq_domanda', 'slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=200))

    def backwards(self, orm):
        # Deleting field 'Domanda.accompagno_html'
        db.delete_column('vsq_domanda', 'accompagno_html')


        # Changing field 'Domanda.accompagno'
        db.alter_column('vsq_domanda', 'accompagno', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Domanda.slug'
        db.alter_column('vsq_domanda', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=100, unique=True))

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
        }
    }

    complete_apps = ['vsq']