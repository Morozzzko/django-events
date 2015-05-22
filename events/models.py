from django.db import models

from django.utils.translation import ugettext_lazy as _


class Event(models.Model):
    name = models.CharField(
        verbose_name=_('Event name'),
        max_length=50
    )
    start_date = models.DateTimeField(verbose_name=_('Start date'))
    end_date = models.DateTimeField(verbose_name=_('End date'))
    description = models.TextField(verbose_name=_('Description'),
                                   default='')

    def __str__(self):
        return self.name

