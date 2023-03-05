from django.contrib import admin

from ads.admin import AnnouncementAdmin
from .models import Properties, House


@admin.register(Properties)
class PropertyAdmin(AnnouncementAdmin):
    list_display = AnnouncementAdmin.list_display + ('square_feet',)
    list_filter = AnnouncementAdmin.list_filter + ('square_feet',)
    search_fields = AnnouncementAdmin.search_fields + ('square_feet',)


@admin.register(House)
class HouseAdmin(PropertyAdmin):
    list_display = PropertyAdmin.list_display + ('bedrooms', 'bathrooms',)
    list_filter = PropertyAdmin.list_filter + ('bedrooms', 'bathrooms',)
    search_fields = PropertyAdmin.search_fields + ('bedrooms', 'bathrooms',)
