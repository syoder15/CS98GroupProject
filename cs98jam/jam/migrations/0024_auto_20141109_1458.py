# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0023_auto_20141109_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='channel',
            name='categories',
            field=models.ManyToManyField(related_name=b'channelCategories', null=True, to='jam.ChannelCategory', blank=True),
            preserve_default=True,
        ),
    ]
