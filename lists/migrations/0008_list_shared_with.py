# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-12-30 06:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lists', '0007_list_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='shared_with',
            field=models.ManyToManyField(related_name='shared_to', to=settings.AUTH_USER_MODEL),
        ),
    ]
