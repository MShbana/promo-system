from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import forms, models

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    add_form = forms.UserAdminCreationForm
    form = forms.UserAdminChangeForm

    list_display = ['username', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    
    fieldsets = (
        ('Login Info', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'address', )}),
        ('Status', {'fields': ('is_active', )}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser',)}),
    )

    add_fieldsets = (
        ('Login Info', {'fields': ('username', 'password', 'password2')}),
    )
    search_fields = ['username']
    ordering = ['username']
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)