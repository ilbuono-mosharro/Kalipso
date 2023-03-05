from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile, Individual, Company


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'u_type', 'is_superuser', 'is_staff', 'is_active', 'first_name', 'last_name',)
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': (
            'first_name', 'last_name', 'u_type', 'email', 'email_confirmation', 'age',
            'terms_and_privacy',)
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined',)}),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email',)
    ordering = ('-date_joined',)


admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'avatar', 'unique_code', 'phone', 'hidden_phone', 'created', 'updated',)
    list_filter = ('user', 'city',)
    search_fields = ('user', 'city',)
    list_per_page = 20
    ordering = ('-created',)


@admin.register(Individual)
class IndividualAdmin(ProfileAdmin):
    list_display = ProfileAdmin.list_display + ('gender',)


@admin.register(Company)
class CompanyAdmin(ProfileAdmin):
    list_display = ProfileAdmin.list_display + ('name', 'vat_number', 'address', 'zip_code',)
    list_filter = ProfileAdmin.list_filter + ('name', 'vat_number',)
    search_fields = ProfileAdmin.search_fields + ('name',)
