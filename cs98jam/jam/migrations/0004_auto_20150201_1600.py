# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0003_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='events',
            field=models.ManyToManyField(to=b'jam.Event', blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='events',
            field=models.ManyToManyField(related_name=b'company_events', to=b'jam.Event', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='events',
            field=models.ManyToManyField(to=b'jam.Event', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='owned_events',
            field=models.ManyToManyField(related_name=b'owned_events', to=b'jam.Event', blank=True),
        ),
    ]
