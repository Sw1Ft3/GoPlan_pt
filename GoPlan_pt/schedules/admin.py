from django.contrib import admin
from .models import Schedule, Event


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'schedule', 'day_of_week', 'start_time', 'end_time']
    list_filter = ['day_of_week', 'schedule']
    search_fields = ['title', 'description']
