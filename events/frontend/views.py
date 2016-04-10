# -*- coding: utf-8 -*-


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from events.models import Event


@login_required
def frontend_view(request):
    event = Event.get_solo()
    return render(request, 'events/frontend/index.html', {
        'site_title': 'Event management',
        'event': event,
    })
