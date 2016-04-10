# -*- coding: utf-8 -*-


from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def frontend_view(request):
    return render(request, 'events/frontend/index.html', {
        'site_title': 'Event management',
    })
