from django.contrib import admin
from .models import Jobs
from ads.admin import StandardAdmin


# # Register your models here.
@admin.register(Jobs)
class AutoMotoAdmin(StandardAdmin):
    list_display = StandardAdmin.list_display + ('schedule', 'level',)
    list_filter = StandardAdmin.list_filter + ('schedule', 'level',)
    search_fields = StandardAdmin.search_fields + ('schedule', 'level',)
