from django.urls import path
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
]