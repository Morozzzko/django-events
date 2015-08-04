# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from django.conf import settings

from django.utils.translation import ugettext_lazy as _

from django.utils.encoding import python_2_unicode_compatible

from phonenumber_field.modelfields import PhoneNumberField

from django_enumfield import enum


class PresenceStatus(enum.Enum):
    ABSENT = 0
    PRESENT = 1
    LEFT = 2

    labels = {
        ABSENT: _('absent'),
        PRESENT: _('present'),
        LEFT: _('left')
    }


@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    additional_name = models.CharField(verbose_name=_('middle name'),
                                      max_length=30,
                                      blank=True)
    telephone = PhoneNumberField(verbose_name=_('phone number'),
                                 blank=True)

    status = enum.EnumField(PresenceStatus,
                            verbose_name=_('presence status'),
                            default=PresenceStatus.ABSENT)

    def __str__(self):
        return str(self.user)


@python_2_unicode_compatible
class Event(models.Model):
    name = models.CharField(
        verbose_name=_('event name'),
        max_length=50
    )
    start_date = models.DateTimeField(verbose_name=_('start date'))
    end_date = models.DateTimeField(verbose_name=_('end date'))
    description = models.TextField(verbose_name=_('description'),
                                   blank=True)
    location = models.CharField(verbose_name=_('location'),
                                max_length=60,
                                blank=True)
    max_team_size = models.PositiveSmallIntegerField(verbose_name=_('maximum team size'),
                                                     default=4)

    def __str__(self):
        return self.name
