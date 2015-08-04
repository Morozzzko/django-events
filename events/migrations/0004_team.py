# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0003_auto_20150716_1909'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('group_ptr', models.OneToOneField(primary_key=True, auto_created=True, serialize=False, parent_link=True, to='auth.Group')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('owner', models.OneToOneField(to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=('auth.group',),
        ),
    ]
