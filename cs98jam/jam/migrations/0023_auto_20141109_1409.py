# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0022_auto_20141105_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='added',
            field=models.DateTimeField(default=datetime.date(2014, 11, 9), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channel',
            name='updated',
            field=models.DateTimeField(default=datetime.date(2014, 11, 9), auto_now=True),
            preserve_default=False,
        ),
    ]
