# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('askapp', '0011_auto_20170110_1905'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thread',
            old_name='sponsored',
            new_name='featured',
        ),
        migrations.AlterField(
            model_name='auditthread',
            name='action',
            field=models.TextField(default='update', choices=[('update', 'Update'), ('close', 'Close'), ('sticky', 'Sticky'), ('hide', 'Hide'), ('delete', 'Delete')]),
        ),
        migrations.AlterField(
            model_name='auditthread',
            name='thread',
            field=models.ForeignKey(to='askapp.Thread'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=markdownx.models.MarkdownxField(null=True),
        ),
        migrations.AlterField(
            model_name='thread',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/images/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='thread',
            name='text',
            field=markdownx.models.MarkdownxField(null=True),
        ),
        migrations.AlterField(
            model_name='thread',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/images/%Y/%m/%d'),
        ),
    ]
