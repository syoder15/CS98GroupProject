# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0017_auto_20141029_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='events',
            field=models.ManyToManyField(to=b'swingtime.Event', blank=True),
        ),
    ]
