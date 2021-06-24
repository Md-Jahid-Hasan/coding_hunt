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
        (_('Role'), {'fields': ('role',)}),
        (_('Social'), {'fields': ('github', 'linkedIn', 'facebook')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        })
    )


admin.site.register(models.User, AdminControl)
