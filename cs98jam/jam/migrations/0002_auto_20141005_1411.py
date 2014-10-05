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
            name='user_id',
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.CharField(default='default', max_length=20),
            preserve_default=False,
        ),
    ]
