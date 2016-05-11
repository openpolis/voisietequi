# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-10 20:43
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.text import slugify
import tinymce.models


def slugify_party_key(apps, schema_editor):
    # We can't import the Partito model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Partito = apps.get_model("vsq", "Partito")
    for party in Partito.objects.all():
        party.party_key = slugify(party.party_key)
        party.save()


class Migration(migrations.Migration):

    dependencies = [
        ('vsq', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(slugify_party_key),
        migrations.AlterField(
            model_name='partito',
            name='party_key',
            field=models.SlugField(max_length=255, unique=True),
        ),

        migrations.AddField(
            model_name='partito',
            name='balance_sheet',
            field=models.CharField(blank=True, max_length=500, verbose_name=b'Dichiarazione patrimoniale'),
        ),
        migrations.AddField(
            model_name='partito',
            name='balance_sheet_document',
            field=models.FileField(blank=True, upload_to=b'dichiarazioni-patrimoniali',
                                   verbose_name=b'Documento della dichiarazione patrimoniale'),
        ),
        migrations.AddField(
            model_name='partito',
            name='description',
            field=tinymce.models.HTMLField(blank=True, verbose_name=b'Biografia'),
        ),
        migrations.AddField(
            model_name='partito',
            name='election_expenses',
            field=models.CharField(blank=True, max_length=500, verbose_name=b'Spese elettorali'),
        ),
        migrations.AddField(
            model_name='partito',
            name='election_expenses_document',
            field=models.FileField(blank=True, upload_to=b'spese-elettorali',
                                   verbose_name=b'Documento delle spese elettorali'),
        ),
        migrations.AddField(
            model_name='partito',
            name='linked_parties',
            field=tinymce.models.HTMLField(blank=True, verbose_name=b'Liste collegate'),
        ),
    ]
