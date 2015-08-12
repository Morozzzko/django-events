# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models, IntegrityError

from django.conf import settings

from django.utils.translation import ugettext_lazy as _

from django.utils.encoding import python_2_unicode_compatible

from django.contrib.auth.models import Group

from django.db.models.signals import post_save

from django.dispatch import receiver

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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def sync_profile(instance, **kwargs):
    """
    Make sure the Profile exists for each User.

    Try to create an object

    :param instance: An instance of 'sender' class that is being saved.
    :type instance: settings.AUTH_USER_MODEL
    :param kwargs: Optional keyword arguments
    :type kwargs: dict
    """
    try:
        TeamMembership.objects.create(user=instance, team=None)
        Profile.objects.create(user=instance, status=PresenceStatus.ABSENT)
    except IntegrityError:
        pass


@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    additional_name = models.CharField(verbose_name=_('middle name'),
                                       max_length=30,
                                       blank=True)

    birth_date = models.DateField(verbose_name=_('birth date'),
                                  blank=True,
                                  null=True)

    telephone = models.CharField(max_length=20,
                                 verbose_name=_('phone number'),
                                 blank=True,
                                 null=True)

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


@python_2_unicode_compatible
class Team(models.Model):
    name = models.TextField(verbose_name=_('team name'),
                            max_length=30)
    description = models.TextField(verbose_name=_('description'))

    curator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                verbose_name=_('curator'),
                                blank=True,
                                null=True,
                                related_name='team_curator')

    def __str__(self):
        return self.name


class TeamMembership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    team = models.ForeignKey(Team,
                             blank=True,
                             null=True)
    role = models.TextField(verbose_name=_('role'),
                            max_length=30,
                            blank=True)
