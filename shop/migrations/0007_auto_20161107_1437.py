# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-07 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20161104_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.FileField(upload_to=b''),
        ),
    ]
