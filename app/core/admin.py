"""
Django admin customization
"""
from django.contrib import admin  # noqa: F401
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models
# Register your models here


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )


admin.site.register(models.User, UserAdmin)
