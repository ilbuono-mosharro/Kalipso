from django.contrib import admin

from .models import Cities


# Register your models here.

@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'slug', 'is_active', 'created_at', 'updated_at',)
    list_filter = ('user', 'is_active', 'created_at', 'updated_at')
    search_fields = ('user', 'name',)
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20
    ordering = ('-created_at',)
