# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0018_auto_20141102_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='notes',
            field=models.TextField(default='N/A'),
            preserve_default=False,
        ),
    ]
