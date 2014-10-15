# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jam', '0004_auto_20141006_1753'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('moniker', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=140)),
                ('is_public', models.BooleanField(default=False)),
                ('admins', models.ManyToManyField(related_name=b'+', to=settings.AUTH_USER_MODEL)),
                ('subscribers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
