from django.contrib import admin
from .models import Auto, Moto
from ads.admin import StandardAdmin


# # Register your models here.
@admin.register(Auto)
class AutoAdmin(StandardAdmin):
    list_display = StandardAdmin.list_display + ('transmission', 'condition', 'ad_type',)
    list_filter = StandardAdmin.list_filter + ('transmission', 'fuel', 'make', 'condition', 'ad_type',)
    search_fields = StandardAdmin.search_fields + ('transmission', 'fuel', 'make',)


@admin.register(Moto)
class MotoAdmin(StandardAdmin):
    list_display = StandardAdmin.list_display + ('transmission', 'condition', 'ad_type',)
    list_filter = StandardAdmin.list_filter + ('transmission', 'fuel', 'condition', 'ad_type',)
    search_fields = StandardAdmin.search_fields + ('transmission', 'fuel', 'make',)
