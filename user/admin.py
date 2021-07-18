from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from . import models


class AdminControl(UserAdmin):
    ordering = ['id']
    list_display = ['email', 'name', 'student_id']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'picture', 'student_id')}),
        (_('Permission'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Role'), {'fields': ('role', 'club_role')}),
        (_('Social'), {'fields': ('bio',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        })
    )


class PositionControl(admin.ModelAdmin):
    ordering = ['-active']
    list_display = ['role', 'active']


admin.site.register(models.User, AdminControl)
admin.site.register(models.ClubPosition, PositionControl)
admin.site.register(models.Link)
