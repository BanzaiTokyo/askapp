# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('askapp', '0005_auto_20161227_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
