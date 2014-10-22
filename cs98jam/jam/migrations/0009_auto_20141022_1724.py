# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0008_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='admins',
            field=models.ManyToManyField(related_name=b'controlledChannels', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
