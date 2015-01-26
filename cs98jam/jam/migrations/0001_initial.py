# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('swingtime', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('admins', models.ManyToManyField(related_name=b'controlledChannels', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChannelAdminNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.CharField(max_length=1000)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('home_channel', models.ForeignKey(related_name=b'adminNotes', to='jam.Channel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChannelCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('count', models.IntegerField(default=0, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('notes', models.TextField(blank=True)),
                ('application_deadline', models.DateField()),
                ('application_status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
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
                ('email', models.CharField(max_length=50)),
                ('employer', models.CharField(max_length=50)),
                ('notes', models.TextField(blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=20)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=60)),
                ('phone_number', models.IntegerField(default=0, blank=True)),
                ('address', models.CharField(max_length=50, blank=True)),
                ('city', models.CharField(max_length=40, blank=True)),
                ('state', models.CharField(max_length=13, blank=True)),
                ('zip_code', models.CharField(max_length=6, blank=True)),
                ('gender', models.CharField(max_length=10, blank=True)),
                ('school', models.CharField(max_length=50, blank=True)),
                ('grad_month', models.CharField(max_length=10, blank=True)),
                ('grad_year', models.IntegerField(default=0, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activation_key', models.CharField(max_length=40)),
                ('key_expires', models.DateTimeField()),
                ('notification_frequency', models.IntegerField(default=0)),
                ('events', models.ManyToManyField(to='swingtime.Event', blank=True)),
                ('owned_events', models.ManyToManyField(related_name=b'owned_events', to='swingtime.Event', blank=True)),
                ('user', models.OneToOneField(related_name=b'profile', to=settings.AUTH_USER_MODEL)),
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
        migrations.AddField(
            model_name='channel',
            name='events',
            field=models.ManyToManyField(to='swingtime.Event', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='channel',
            name='subscribers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, blank=True),
            preserve_default=True,
        ),
    ]
