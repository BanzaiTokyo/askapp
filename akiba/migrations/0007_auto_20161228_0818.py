# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('akiba', '0006_post_deleted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='tag_name',
            new_name='name',
        ),
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(default='', max_length=60),
            preserve_default=False,
        ),
    ]
