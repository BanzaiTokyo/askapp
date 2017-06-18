# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('askapp', '0014_auto_20170529_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='domain',
            field=models.CharField(max_length=255, blank=True, null=True),
        ),
    ]
