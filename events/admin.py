# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from solo.admin import SingletonModelAdmin

from .models import Event, Profile, Team, Event, TeamMembership


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(SingletonModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    pass
