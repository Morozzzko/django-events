# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('middleName', models.CharField(verbose_name='middle name', blank=True, max_length=30)),
                ('phoneNumber', phonenumber_field.modelfields.PhoneNumberField(verbose_name='phone number', blank=True, max_length=128)),
                ('status', models.IntegerField(verbose_name='presence status', default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='attendee',
            name='event',
        ),
        migrations.RemoveField(
            model_name='attendee',
            name='user',
        ),
        migrations.RemoveField(
            model_name='organizer',
            name='event',
        ),
        migrations.RemoveField(
            model_name='organizer',
            name='user',
        ),
        migrations.RemoveField(
            model_name='event',
            name='attendees',
        ),
        migrations.RemoveField(
            model_name='event',
            name='organizers',
        ),
        migrations.DeleteModel(
            name='Attendee',
        ),
        migrations.DeleteModel(
            name='Organizer',
        ),
    ]
