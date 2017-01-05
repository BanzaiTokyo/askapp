# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('askapp', '0008_auto_20161228_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='tags',
            field=models.ManyToManyField(to='askapp.Tag', blank=True),
        ),
    ]
