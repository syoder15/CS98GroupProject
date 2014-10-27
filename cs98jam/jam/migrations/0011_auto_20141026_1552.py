# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0010_channeladminnote'),
    ]

    operations = [
        migrations.RenameField(
            model_name='channeladminnote',
            old_name='channel',
            new_name='home_channel',
        ),
    ]
