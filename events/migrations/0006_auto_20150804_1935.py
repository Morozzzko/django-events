# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20150804_1608'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='middleName',
            new_name='additionalName',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='phoneNumber',
            new_name='telephone',
        ),
    ]
