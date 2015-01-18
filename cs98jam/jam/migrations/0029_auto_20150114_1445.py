# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swingtime', '__first__'),
        ('jam', '0028_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='owned_events',
            field=models.ManyToManyField(related_name=b'owned_events', to='swingtime.Event', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]
