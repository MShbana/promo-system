from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = 'accounts'


urlpatterns = [
    path(
        'register-admin-user/',
        views.RegisterAdminUser.as_view(),
        name='register_admin_user',
    ),
    path(
        'register-normal-user/',
        views.RegisterNormalUser.as_view(),
        name='register_normal_user',
    ),
    path(
        'login/',
        obtain_auth_token,
        name='login',
    )
]
