# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20150809_0203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='members',
        ),
        migrations.AlterField(
            model_name='teammembership',
            name='team',
            field=models.ForeignKey(null=True, blank=True, to='events.Team'),
        ),
        migrations.AlterField(
            model_name='teammembership',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
