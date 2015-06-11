from django.contrib import admin

from .models import Event, Attendee, Organizer


class AttendeeInline(admin.TabularInline):
    model = Attendee


class OrganizerInline(admin.TabularInline):
    model = Organizer


class EventAdmin(admin.ModelAdmin):
    inlines = [
        AttendeeInline,
        OrganizerInline,
    ]

admin.site.register(Event, EventAdmin)
