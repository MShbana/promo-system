from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import (
    PromoAdminUser,
    PromoNormalUser
)


app_name = 'promos'

router = DefaultRouter()

router.register(
    r'admin-user',
    PromoAdminUser,
    basename='promo_admin_user'
)
router.register(
    r'normal-user',
    PromoNormalUser,
    basename='promo_normal_user'
)

urlpatterns = router.urls
