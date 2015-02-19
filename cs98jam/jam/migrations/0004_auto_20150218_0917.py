# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jam', '0003_auto_20150217_2110'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventOccurrence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('frequency', models.CharField(max_length=10)),
                ('start_month', models.IntegerField()),
                ('start_year', models.IntegerField()),
                ('start_day', models.IntegerField()),
                ('day_of_the_week', models.CharField(max_length=10)),
                ('end_date', models.DateField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='occurrence_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
