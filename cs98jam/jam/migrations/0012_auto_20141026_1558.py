# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0011_auto_20141026_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channeladminnote',
            name='home_channel',
            field=models.ForeignKey(related_name=b'adminNotes', to='jam.Channel'),
        ),
    ]
