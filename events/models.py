# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from django.conf import settings

from django.utils.translation import ugettext_lazy as _

from django.utils.encoding import python_2_unicode_compatible

from django.db.models.signals import post_save

from django.core.exceptions import ValidationError

from django.dispatch import receiver

from django_enumfield import enum

from solo.models import SingletonModel


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
    TeamMembership.objects.get_or_create(user=instance, defaults={'team': None})
    Profile.objects.get_or_create(user=instance)
    PresenceStatus.objects.get_or_create(user=instance)


@python_2_unicode_compatible
class PresenceStatus(models.Model):
    class Options(enum.Enum):
        ABSENT = 0
        PRESENT = 1
        LEFT = 2

        labels = {
            ABSENT: _('absent'),
            PRESENT: _('present'),
            LEFT: _('left')
        }

    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    status = enum.EnumField(Options,
                            default=Options.ABSENT,
                            verbose_name=_('status'))

    last_modified = models.DateTimeField(verbose_name=_("last-modified"),
                                         auto_now=True)

    def __str__(self):
        return _("{user} ({status})").format(user=self.user,
                                             status=PresenceStatus.Options.label(self.status))


@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    middle_name = models.CharField(verbose_name=_('middle name'),
                                   max_length=30,
                                   blank=True)

    birth_date = models.DateField(verbose_name=_('birth date'),
                                  blank=True,
                                  null=True)

    telephone = models.CharField(max_length=20,
                                 verbose_name=_('phone number'),
                                 blank=True,
                                 null=True)

    def __str__(self):
        return self.user


@python_2_unicode_compatible
class Event(SingletonModel):
    name = models.CharField(
        verbose_name=_('event name'),
        max_length=50
    )
    start_date = models.DateTimeField(verbose_name=_('start date'),
                                      blank=True,
                                      null=True)
    end_date = models.DateTimeField(verbose_name=_('end date'),
                                    blank=True,
                                    null=True)
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


@python_2_unicode_compatible
class TeamMembership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    team = models.ForeignKey(Team,
                             blank=True,
                             null=True)
    role = models.TextField(verbose_name=_('role'),
                            max_length=30,
                            blank=True)

    def clean(self):
        event = Event.get_solo()
        if len(TeamMembership.objects.filter(team=self.team)) >= event.max_team_size:
            raise ValidationError(_("team membership is limited to {max} members").format(max=event.max_team_size))
        super(TeamMembership, self).clean()

    def __str__(self):
        return str("{user} ({team})").format(user=self.user, team=self.team)
