# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-12 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vsq', '0002_auto_20160510_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='partito',
            name='is_module_open',
            field=models.BooleanField(default=True, verbose_name=b'Questionario aperto/chiuso'),
        ),
    ]