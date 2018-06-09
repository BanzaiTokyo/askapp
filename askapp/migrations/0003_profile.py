# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import askapp.models
from django.conf import settings
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('askapp', '0002_thread_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', askapp.models.AskappImageField(storage=askapp.models.OverwriteStorage(), upload_to=askapp.models.avatar_name_path, blank=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('city', models.CharField(max_length=50, blank=True)),
                ('about', models.TextField(max_length=500, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
    ]
