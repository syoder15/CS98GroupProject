# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0012_auto_20141026_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='channeladminnote',
            name='created_at',
            field=models.DateTimeField(default=datetime.date(2014, 10, 26), auto_now_add=True),
            preserve_default=False,
        ),
    ]
