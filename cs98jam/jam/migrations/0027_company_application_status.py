# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0026_auto_20150112_2330'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='application_status',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
