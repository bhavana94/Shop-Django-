# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-04 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20161104_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(upload_to=b'myshopup/media/'),
        ),
    ]
