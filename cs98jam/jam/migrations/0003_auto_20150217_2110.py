# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0002_auto_20150208_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='application_deadline',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone_number',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
