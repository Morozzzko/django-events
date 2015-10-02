# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20150813_1607'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='additional_name',
            new_name='middle_name',
        ),
    ]
