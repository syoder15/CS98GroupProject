# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jam', '0009_auto_20141022_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelAdminNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=1000)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('channel', models.ForeignKey(to='jam.Channel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
