# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^groups/$', views.TeamList.as_view(), name='team-list'),
    url(r'^groups/(?P<pk>[0-9]+)/$', views.TeamDetail.as_view(), name='team-detail'),

]