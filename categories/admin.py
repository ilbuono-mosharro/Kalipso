from django.contrib import admin
from .models import Category, SubCategory


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'slug', 'is_active', 'icon', 'created_at', 'updated_at',)
    list_filter = ('user', 'is_active', 'created_at', 'updated_at')
    search_fields = ('user', 'name',)
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20
    ordering = ('-created_at',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'slug', 'is_active', 'created_at', 'updated_at',)
    list_filter = ('user', 'category', 'is_active', 'created_at', 'updated_at')
    search_fields = ('user', 'name',)
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20
    ordering = ('-created_at',)
