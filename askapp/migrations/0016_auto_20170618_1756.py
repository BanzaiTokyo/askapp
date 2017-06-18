# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('askapp', '0015_thread_domain'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThreadFavorite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('thread', models.ForeignKey(to='askapp.Thread')),
                ('user', models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='threadfavorite',
            unique_together=set([('user', 'thread')]),
        ),
    ]
