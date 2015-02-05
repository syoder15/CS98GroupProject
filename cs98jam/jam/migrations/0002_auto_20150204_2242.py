# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='grad_month',
            field=models.CharField(max_length=15, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(max_length=11, blank=True),
        ),
    ]
