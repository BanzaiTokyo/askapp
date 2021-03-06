# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(to='askapp.Post', null=True, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('taken_on', models.DateTimeField(auto_now_add=True)),
                ('action_name', models.TextField(choices=[('update', 'Update'), ('close', 'Close'), ('sticky', 'Sticky')], default='update')),
                ('old_text', models.TextField(null=True)),
                ('old_title', models.TextField(null=True)),
                ('post', models.ForeignKey(to='askapp.Post', null=True, on_delete=models.CASCADE)),
                ('taken_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('hidden', models.BooleanField(default=False)),
                ('closed', models.BooleanField(default=False)),
                ('sticky', models.DateField(null=True)),
                ('sponsored', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('thread_type', models.CharField(choices=[('QQ', 'Question'), ('DD', 'Discussion'), ('LL', 'Link')], default='DD', null=True, max_length=2)),
                ('text', models.TextField(null=True)),
                ('title', models.CharField(null=True, max_length=255)),
                ('image', models.ImageField(upload_to='uploads/images/%Y/%m/%d')),
                ('score', models.IntegerField(default=0)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)),
                ('tags', models.ManyToManyField(to='askapp.Tag')),
                ('link', models.URLField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='thread_id',
            field=models.ForeignKey(to='askapp.Thread', null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='post',
            name='text',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='the_answer',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('points', models.IntegerField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='ThreadLike',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('points', models.IntegerField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)),
            ],
        ),
    ]
