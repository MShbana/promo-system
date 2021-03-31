from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    RegisterAdminUser,
    RegisterNormalUser
)

app_name = 'accounts'


urlpatterns = [
    path(
        'register-admin-user/',
        RegisterAdminUser.as_view(),
        name='register_admin_user',
    ),
    path(
        'register-normal-user/',
        RegisterNormalUser.as_view(),
        name='register_normal_user',
    ),
    path(
        'login/',
        obtain_auth_token,
        name='login',
    )
]
