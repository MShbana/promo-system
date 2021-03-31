from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import (
    UserAdminChangeForm,
    UserAdminCreationForm
)
from .models import (
    NormalUser,
    AdministratorUser
)


User = get_user_model()


class UserAdmin(BaseUserAdmin):
    add_form = UserAdminCreationForm
    form = UserAdminChangeForm

    add_fieldsets = (
        ('Login Info', {'fields': ('username', 'password', 'password2')}),
    )

    fieldsets = (
        ('Login Info', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', )}),
        ('Status', {'fields': ('is_active', )}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser',)}),
        ('Dates', {'fields': ('last_login', 'date_joined',)}),

    )

    list_display = [
        'username',
        'is_active',
        'is_staff',
        'is_superuser'
    ]
    list_filter = [
        'is_active',
        'is_staff',
        'is_superuser'
    ]

    readonly_fields = [
        'last_login',
        'date_joined',
    ]
    search_fields = [
        'username'
    ]


class NormalUserAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'mobile_number',
        'address',
    ]
    
    list_filter = [
        'user__last_login',
        'user__date_joined',
    ]
    search_fields = [
        'user__username',
        'user__name',
    ]

class AdministratorUserAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'address',
    ]
    
    list_filter = [
        'user__last_login',
        'user__date_joined',
    ]
    search_fields = [
        'user__username',
        'user__name',
    ]


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(NormalUser, NormalUserAdmin)
admin.site.register(AdministratorUser, AdministratorUserAdmin)
