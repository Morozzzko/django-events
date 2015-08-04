# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20150804_1935'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='additionalName',
            new_name='additional_name',
        ),
    ]
