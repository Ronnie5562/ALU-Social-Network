"""
Django admin config file
"""

from core import models
from django.contrib import admin
from django.utils.translation import gettext as translate_text
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    """
    Admin Config for the user model
    """
    ordering = ['id']
    list_display = ['id', 'full_name', 'email', 'user_role']
    readonly_fields = ['last_login']

    fieldsets = (
        (
            None,
            {
                'fields': ('email', 'password')
            }
        ),
        (
            translate_text('Personal Information'),
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'short_bio',
                    'about_me',
                    'user_role',
                    'intake',
                    'professional_role',
                    'current_company',

                )
            }
        ),
        (
            translate_text('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser'
                )
            }
        ),
        (
            translate_text('Important dates'),
            {
                'fields': (
                    'last_login',
                )
            }
        )
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'first_name',
                    'last_name',
                    'short_bio',
                    'about_me',
                    'user_role',
                    'intake',
                    'professional_role',
                    'current_company',
                    'is_staff',
                    'is_active',
                    'is_superuser',
                )
            }
        ),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Link)