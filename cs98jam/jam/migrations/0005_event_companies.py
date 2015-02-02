# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0004_auto_20150201_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='companies',
            field=models.CharField(default=b'', max_length=200),
            preserve_default=True,
        ),
    ]
