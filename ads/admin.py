from django.contrib import admin
from .models import Announcement, Standard, Image


# Register your models here.
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('profile', 'title', 'created_at', 'updated_at',)
    list_filter = ('profile', 'category', 'subcategory',)
    search_fields = ('profile', 'title',)
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 10
    ordering = ('-created_at',)


@admin.register(Standard)
class StandardAdmin(admin.ModelAdmin):
    list_display = ('profile', 'title', 'created_at', 'updated_at',)
    list_filter = ('profile', 'category', 'subcategory',)
    search_fields = ('profile', 'title',)
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20
    ordering = ('-created_at',)


@admin.register(Image)
class AnnouncementImageAdmin(admin.ModelAdmin):
    list_display = ('profile', 'announcement', 'created_at', 'updated_at',)
    list_filter = ('profile', 'announcement')
    search_fields = ('profile', 'announcement',)
    list_per_page = 20
    ordering = ('-created_at',)
