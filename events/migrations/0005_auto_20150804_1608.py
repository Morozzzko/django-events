# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('events', '0004_team'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='group_ptr',
        ),
        migrations.RemoveField(
            model_name='team',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]
