# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='event name', max_length=50)),
                ('start_date', models.DateTimeField(verbose_name='start date')),
                ('end_date', models.DateTimeField(verbose_name='end date')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('location', models.CharField(verbose_name='location', blank=True, max_length=60)),
                ('max_team_size', models.PositiveSmallIntegerField(default=4, verbose_name='maximum team size')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('additional_name', models.CharField(verbose_name='middle name', blank=True, max_length=30)),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(verbose_name='phone number', blank=True, max_length=128)),
                ('status', models.IntegerField(default=0, verbose_name='presence status')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('description', models.TextField(verbose_name='description')),
                ('group', models.OneToOneField(to='auth.Group')),
                ('owner', models.ForeignKey(verbose_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
