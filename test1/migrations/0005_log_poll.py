# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-20 09:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0004_auto_20160620_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='poll',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='test1.Request'),
        ),
    ]
