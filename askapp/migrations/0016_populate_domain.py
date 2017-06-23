# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_domain(apps, schema_editor):
    threads = apps.get_model('askapp', 'Thread')
    for thread in threads.objects.all():
        thread.save()


class Migration(migrations.Migration):

    dependencies = [
        ('askapp', '0015_thread_domain'),
    ]

    operations = [
        migrations.RunPython(populate_domain, migrations.RunPython.noop)
    ]
