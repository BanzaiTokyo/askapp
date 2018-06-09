# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('askapp', '0007_auto_20161228_0818'),
    ]

    operations = [
        migrations.AddField(
            model_name='postlike',
            name='post',
            field=models.ForeignKey(default=1, to='askapp.Post', on_delete=models.CASCADE),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='threadlike',
            name='thread',
            field=models.ForeignKey(default=1, to='askapp.Thread', on_delete=models.CASCADE),
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
