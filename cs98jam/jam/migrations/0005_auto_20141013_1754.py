# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0004_auto_20141006_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='email',
            field=models.CharField(default='poop@poop.com', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='employer',
            field=models.CharField(default='Garbageman', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='user',
            field=models.CharField(default='thebaconsmith13', max_length=20),
            preserve_default=False,
        ),
    ]
