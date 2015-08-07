# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin


from .models import Event, Profile, Team


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass
