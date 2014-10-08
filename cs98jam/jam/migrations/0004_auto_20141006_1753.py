# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(max_length=40, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='grad_month',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='grad_year',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='school',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='state',
            field=models.CharField(max_length=13, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='zip_code',
            field=models.CharField(max_length=6, blank=True),
        ),
    ]
