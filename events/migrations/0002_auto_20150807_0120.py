# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamConnection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.TextField(blank=True, max_length=30, verbose_name='role')),
            ],
        ),
        migrations.RemoveField(
            model_name='team',
            name='group',
        ),
        migrations.RemoveField(
            model_name='team',
            name='owner',
        ),
        migrations.AddField(
            model_name='team',
            name='curator',
            field=models.ForeignKey(related_name='team_curator', to=settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name='curator'),
        ),
        migrations.AddField(
            model_name='team',
            name='name',
            field=models.TextField(default='', max_length=30, verbose_name='team name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teamconnection',
            name='team',
            field=models.ForeignKey(to='events.Team'),
        ),
        migrations.AddField(
            model_name='teamconnection',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(through='events.TeamConnection', to=settings.AUTH_USER_MODEL, related_name='team_members'),
        ),
    ]
