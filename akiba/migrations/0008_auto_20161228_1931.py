# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('akiba', '0007_auto_20161228_0818'),
    ]

    operations = [
        migrations.AddField(
            model_name='postlike',
            name='post',
            field=models.ForeignKey(default=1, to='akiba.Post'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='threadlike',
            name='thread',
            field=models.ForeignKey(default=1, to='akiba.Thread'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='postlike',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='threadlike',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
