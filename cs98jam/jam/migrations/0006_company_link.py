# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0005_event_companies'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='link',
            field=models.CharField(default='http://www.google.com', max_length=150, blank=True),
            preserve_default=False,
        ),
    ]
