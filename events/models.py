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
    head_organizer = models.ForeignKey(User, verbose_name=_('head organizer'))

    def __str__(self):
        return self.name

