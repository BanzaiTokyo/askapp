# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('askapp', '0009_auto_20170105_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='sticky',
            field=models.DateField(null=True, blank=True),
        ),
    ]
