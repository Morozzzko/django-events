# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_profile_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='telephone',
            field=models.CharField(max_length=20, null=True, verbose_name='phone number', blank=True),
        ),
    ]
