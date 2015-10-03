# -*- coding: utf-8 -*-


from django.conf.urls import url, include
from events.api.frontend import views

urlpatterns = [
    url(r'^', views.frontend_view, name='api'),
]