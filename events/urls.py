# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from . import views
from .utils import add_optional_trailing_slashes

router = DefaultRouter()

user_list = views.UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

user_detail = views.UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_status = views.StatusViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
})

user_team = views.TeamMembershipViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
})

team_list = views.TeamViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

team_detail = views.TeamViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns(
    add_optional_trailing_slashes([
        url(r'^users/$', user_list, name='user-list'),
        url(r'^users/attendees/$', user_list, {'type': 'attendees'}, name='user-list'),
        url(r'^users/organizers/$', user_list, {'type': 'organizers'}, name='user-list'),
        url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
        url(r'^users/(?P<pk>[0-9]+)/status/$', user_status, name='user-status'),
        url(r'^groups/$', team_list, name='team-list'),
        url(r'^groups/(?P<pk>[0-9]+)/$', team_detail, name='team-detail'),
    ]), allowed=['json', 'html'])
