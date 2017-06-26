# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse

def populate_domain(apps, schema_editor):
    threads = apps.get_model('askapp', 'Thread')
    for thread in threads.objects.all():
        if thread.link:
            hostname = urlparse(thread.link)
            thread.domain = hostname.netloc
            thread.save()


class Migration(migrations.Migration):

    dependencies = [
        ('askapp', '0015_thread_domain'),
    ]

    operations = [
        migrations.RunPython(populate_domain, migrations.RunPython.noop)
    ]
