# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    # replaces = [('akiba', '0001_squashed_0005_auto_20161201_2038'), ('akiba', '0002_auto_20161201_2053')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255, null=True)),
                ('text', models.TextField()),
                ('author', models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL)),
                ('closed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True)),
                ('hidden', models.BooleanField(default=False)),
                ('image', models.FileField(upload_to=b'uploads/images/%Y/%m/%d/%H/%M/%S/')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(to='akiba.Post', null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('sponsored', models.BooleanField(default=False)),
                ('sticky', models.BooleanField(default=False)),
                ('texthtml', models.TextField(null=True)),
                ('thread_type', models.CharField(default=b'DD', null=True, max_length=2, choices=[(b'QQ', b'Question'), (b'DD', b'Discussion'), (b'LL', b'Link')])),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('tag_name', models.CharField(max_length=60)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='akiba.Tag'),
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('taken_on', models.DateTimeField(auto_now_add=True)),
                ('action_name', models.TextField(default='update', choices=[('update', 'Update'), ('close', 'Close'), ('sticky', 'Sticky')])),
                ('old_text_html', models.TextField(null=True)),
                ('old_text', models.TextField(null=True)),
                ('old_title', models.TextField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.FileField(upload_to='uploads/images/%Y/%m/%d/%H/%M/%S/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='parent',
            field=models.ForeignKey(to='akiba.Post', null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='sticky',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='thread_type',
            field=models.CharField(default='DD', null=True, max_length=2, choices=[('QQ', 'Question'), ('DD', 'Discussion'), ('LL', 'Link')]),
        ),
        migrations.AddField(
            model_name='action',
            name='post',
            field=models.ForeignKey(to='akiba.Post', null=True),
        ),
        migrations.AddField(
            model_name='action',
            name='takeby_by',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
