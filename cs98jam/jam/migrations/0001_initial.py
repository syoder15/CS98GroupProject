# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('phone_number', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField(default=0)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=60)),
                ('phone_number', models.IntegerField(default=0)),
                ('address', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=40)),
                ('state', models.CharField(max_length=13)),
                ('zip_code', models.CharField(max_length=6)),
                ('gender', models.CharField(max_length=10)),
                ('school', models.CharField(max_length=50)),
                ('grad_month', models.CharField(max_length=10)),
                ('grad_year', models.IntegerField(default=0, max_length=5)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
