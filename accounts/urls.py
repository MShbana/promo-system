from django.urls import path
from . import views

app_name = 'accounts'


urlpatterns = [
    path(
        'register-admin/',
        views.RegisterAdminUser.as_view(),
        name='register_admin',
    ),
]