# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swingtime', '__first__'),
        ('jam', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='events',
            field=models.ManyToManyField(related_name=b'company_events', to='swingtime.Event', blank=True),
            preserve_default=True,
        ),
    ]
