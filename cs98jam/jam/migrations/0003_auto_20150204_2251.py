# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0002_auto_20150204_2242'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='grad_month',
            new_name='grad_date',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='grad_year',
        ),
    ]
