# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'EarlyBird', fields ['email']
        db.create_unique('vsq_earlybird', ['email'])


    def backwards(self, orm):
        # Removing unique constraint on 'EarlyBird', fields ['email']
        db.delete_unique('vsq_earlybird', ['email'])


    models = {
        'vsq.domanda': {
            'Meta': {'object_name': 'Domanda'},
            'accompagno': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'accompagno_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'approfondimento': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'approfondimento_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ordine': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'}),
            'testo': ('django.db.models.fields.TextField', [], {}),
            'testo_html': ('django.db.models.fields.TextField', [], {})
        },
        'vsq.earlybird': {
            'Meta': {'object_name': 'EarlyBird'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'vsq.partito': {
            'Meta': {'object_name': 'Partito'},
            'coalizione': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'colore': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'denominazione': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'responsabile_email': ('django.db.models.fields.EmailField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'responsabile_nome': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'risposte_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'sigla': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'simbolo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sito': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'})
        },
        'vsq.rispostapartito': {
            'Meta': {'object_name': 'RispostaPartito'},
            'domanda': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vsq.Domanda']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nonorig': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'partito': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vsq.Partito']"}),
            'risposta_int': ('django.db.models.fields.SmallIntegerField', [], {}),
            'risposta_txt': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'vsq.rispostautente': {
            'Meta': {'object_name': 'RispostaUtente'},
            'domanda': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vsq.Domanda']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'risposta_int': ('django.db.models.fields.SmallIntegerField', [], {}),
            'utente': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vsq.Utente']"})
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