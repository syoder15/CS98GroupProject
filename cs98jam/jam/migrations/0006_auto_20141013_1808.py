# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0005_auto_20141013_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='application_deadline',
            field=models.DateField(default=datetime.date(2014, 10, 13)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='user',
            field=models.CharField(default='thebaconsmith13', max_length=20),
            preserve_default=False,
        ),
    ]
