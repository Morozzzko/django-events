# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20150816_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='telephone',
            field=models.CharField(default='', blank=True, verbose_name='phone number', max_length=20),
            preserve_default=False,
        ),
    ]
