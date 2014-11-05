# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swingtime', '__first__'),
        ('jam', '0018_auto_20141102_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='events',
            field=models.ManyToManyField(to='swingtime.Event', blank=True),
            preserve_default=True,
        ),
    ]
