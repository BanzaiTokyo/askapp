# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('askapp', '0010_auto_20170106_0657'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditThread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.TextField(default=b'update', choices=[(b'update', b'Update'), (b'close', b'Close'), (b'sticky', b'Sticky'), (b'hide', b'Hide'), (b'delete', b'Delete')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='thread',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='auditthread',
            name='thread',
            field=models.ForeignKey(to='askapp.Thread', on_delete=django.db.models.deletion.DO_NOTHING),
        ),
        migrations.AddField(
            model_name='auditthread',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
        ),
    ]
