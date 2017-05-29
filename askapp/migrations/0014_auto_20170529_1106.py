# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('askapp', '0013_auto_20170206_0748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='tags',
            field=models.ManyToManyField(verbose_name='tags', blank=True, to='askapp.Tag'),
        ),
    ]
