from django.contrib import admin

from django_school.apps.events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
