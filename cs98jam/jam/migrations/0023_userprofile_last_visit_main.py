# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0022_auto_20141105_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_visit_main',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
