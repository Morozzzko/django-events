# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150716_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.CharField(verbose_name='location', blank=True, max_length=60),
        ),
        migrations.AddField(
            model_name='event',
            name='max_team_size',
            field=models.PositiveSmallIntegerField(verbose_name='maximum team size', default=4),
        ),
    ]
