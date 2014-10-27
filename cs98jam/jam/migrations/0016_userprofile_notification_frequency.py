# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0015_auto_20141026_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='notification_frequency',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
