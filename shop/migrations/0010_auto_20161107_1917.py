# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-07 19:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20161107_1556'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='disscount',
            new_name='discount',
        ),
    ]
