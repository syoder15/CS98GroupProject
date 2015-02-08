# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='grad_month',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='grad_year',
        ),
        migrations.AddField(
            model_name='profile',
            name='grad_date',
            field=models.CharField(default='June, 2015', max_length=15, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(max_length=11, blank=True),
        ),
    ]
