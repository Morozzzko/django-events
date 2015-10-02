# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0002_auto_20150807_0120'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.TextField(blank=True, max_length=30, verbose_name='role')),
            ],
        ),
        migrations.RemoveField(
            model_name='teamconnection',
            name='team',
        ),
        migrations.RemoveField(
            model_name='teamconnection',
            name='user',
        ),
        migrations.AlterField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='events.TeamMembership', related_name='team_members'),
        ),
        migrations.DeleteModel(
            name='TeamConnection',
        ),
        migrations.AddField(
            model_name='teammembership',
            name='team',
            field=models.ForeignKey(to='events.Team'),
        ),
        migrations.AddField(
            model_name='teammembership',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
