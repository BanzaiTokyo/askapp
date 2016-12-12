# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('akiba', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='thumbnail',
            field=models.FileField(upload_to='uploads/images/%Y/%m/%d/%H/%M/%S/', null=True),
        ),
    ]
