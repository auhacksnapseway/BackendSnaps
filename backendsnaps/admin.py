from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Event, DrinkEvent


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	pass


@admin.register(DrinkEvent)
class DrinkEventAdmin(admin.ModelAdmin):
	pass


admin.site.register(User, UserAdmin)
