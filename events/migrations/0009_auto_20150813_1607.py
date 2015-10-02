# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20150813_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='presencestatus',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 13, 13, 7, 14, 804545, tzinfo=utc), verbose_name='last-modified', auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='presencestatus',
            name='status',
            field=models.IntegerField(default=0, verbose_name='status'),
        ),
    ]
