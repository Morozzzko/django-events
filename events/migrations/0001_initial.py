# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('status', models.CharField(verbose_name='status', max_length=15, choices=[('pending', 'pending'), ('registered', 'registered'), ('attended', 'attended'), ('left', 'left')])),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='event name', max_length=50)),
                ('start_date', models.DateTimeField(verbose_name='start date')),
                ('end_date', models.DateTimeField(verbose_name='end date')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('attendees', models.ManyToManyField(through='events.Attendee', verbose_name='attendees', related_name='event_attendees', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('role', models.CharField(verbose_name='role', max_length=15, choices=[('head', 'head'), ('regular', 'regular')])),
                ('event', models.ForeignKey(to='events.Event')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='organizers',
            field=models.ManyToManyField(through='events.Organizer', verbose_name='organizers', related_name='event_organizers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attendee',
            name='event',
            field=models.ForeignKey(to='events.Event'),
        ),
        migrations.AddField(
            model_name='attendee',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
