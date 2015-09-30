# -*- coding: utf-8 -*-

# ^login/$ [name='login']
# ^logout/$ [name='logout']
# ^password_change/$ [name='password_change']
# ^password_change/done/$ [name='password_change_done']
# ^password_reset/$ [name='password_reset']
# ^password_reset/done/$ [name='password_reset_done']
# ^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$ [name='password_reset_confirm']
# ^reset/done/$ [name='password_reset_complete']

from django.conf.urls import include, url
from events.frontend import views

urlpatterns = [
    url(r'^login/$', views.sample, name='login'),
    url(r'^logout/$', views.sample, name='logout'),
    url(r'^password_change/$', views.sample, name='password_change'),
    url(r'^password_change/done/$', views.sample, name='password_change_done'),
    url(r'^password_reset/$', views.sample, name='password_reset'),
    url(r'^password_reset/done/$', views.sample, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.sample, name='password_reset_confirm'),
    url(r'^reset/done/$', views.sample, name='password_reset_complete'),
]
