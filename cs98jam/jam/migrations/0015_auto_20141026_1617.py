# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0014_auto_20141026_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channeladminnote',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
