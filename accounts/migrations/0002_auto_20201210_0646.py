# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-12-09 21:46
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='uid',
            field=models.CharField(default=uuid.uuid4, max_length=40),
        ),
    ]
