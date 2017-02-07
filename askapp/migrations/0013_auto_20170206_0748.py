# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('askapp', '0012_auto_20170203_1436'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='the_answer',
            new_name='is_answer',
        ),
        migrations.AddField(
            model_name='post',
            name='accepted',
            field=models.DateTimeField(null=True),
        ),
    ]
