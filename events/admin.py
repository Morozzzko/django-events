# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from django.contrib.auth.models import User

from .models import Event, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


admin.site.unregister(User)


@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [
        ProfileInline,
    ]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
