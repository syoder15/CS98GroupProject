# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0013_channeladminnote_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channeladminnote',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 26, 16, 9, 24, 822000)),
        ),
    ]
