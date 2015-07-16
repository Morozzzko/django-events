# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

from django.utils.encoding import python_2_unicode_compatible


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
    organizer_groups = models.ManyToManyField(User,
                                              through='Organizer',
                                              through_fields=['event', 'user'],
                                              verbose_name=_('organizers'),
                                              related_name='event_organizers')

    attendees = models.ManyToManyField(User,
                                       through='Attendee',
                                       through_fields=['event', 'user'],
                                       verbose_name=_('attendees'),
                                       related_name='event_attendees')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Attendee(models.Model):
    """
    Attendee is a user attending an event.

    Attendees have several statuses:

        1. Registration pending (Status.PENDING) -- used whenever organizer needs to personally accept or reject people
        2. Registered/Registration accepted (status.REGISTERED)
        3. Attended (status.ATTENDED) -- used to mark person's presence at the event
        4. Left (status.LEFT) -- used to mark people who left the event for various reasons
    """

    class Status:
        PENDING = 'pending'
        REGISTERED = 'registered'
        ATTENDED = 'attended'
        LEFT = 'left'

        choices = (
            (PENDING, 'pending'),
            (REGISTERED, 'registered'),
            (ATTENDED, 'attended'),
            (LEFT, 'left'),
        )

    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    status = models.CharField(max_length=15,
                              choices=Status.choices,
                              verbose_name=_('status'))

    def __str__(self):
        return _('{user} status on {event}: {status}') % {
            'user': self.user.username,
            'event': str(self.event),
            'status': _(self.status),
        }


@python_2_unicode_compatible
class Organizer(models.Model):
    class Roles:
        HEAD = 'head'
        REGULAR = 'regular'

        choices = (
            (HEAD, 'head'),
            (REGULAR, 'regular')
        )

    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    role = models.CharField(max_length=15,
                            choices=Roles.choices,
                            verbose_name=_('role'))

    def __str__(self):
        return _('{event} organizer ({role}) {user} ') % {
            'user': self.user.username,
            'event': str(self.event),
            'role': _(self.role),

        }
