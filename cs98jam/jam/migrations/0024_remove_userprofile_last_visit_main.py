# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0023_userprofile_last_visit_main'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='last_visit_main',
        ),
    ]
