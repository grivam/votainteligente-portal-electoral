# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-24 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_candidate', '0009_auto_20171024_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateincremental',
            name='used',
            field=models.BooleanField(default=False),
        ),
    ]