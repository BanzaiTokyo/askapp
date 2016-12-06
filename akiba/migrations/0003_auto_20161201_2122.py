# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('akiba', '0002_post_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
