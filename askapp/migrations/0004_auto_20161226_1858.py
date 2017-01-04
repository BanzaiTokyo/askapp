# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('askapp', '0003_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='action',
            old_name='taken_by',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='thread',
            old_name='author',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='post',
            name='thread_id',
        ),
        migrations.AddField(
            model_name='post',
            name='thread',
            field=models.ForeignKey(default=1, to='askapp.Thread'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='thread',
            name='image',
            field=models.ImageField(null=True, upload_to=b'uploads/images/%Y/%m/%d', blank=True),
        ),
        migrations.AlterField(
            model_name='thread',
            name='link',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='thread',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to=b'uploads/images/%Y/%m/%d', blank=True),
        ),
    ]
