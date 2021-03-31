from rest_framework.routers import DefaultRouter
from django.urls import path

from . import views


router = DefaultRouter()

router.register(
    r'admin-user',
    views.PromoAdminUser,
    basename='promo_admin_user'
)
router.register(
    r'normal-user',
    views.PromoNormalUser,
    basename='promo_normal_user'
)

urlpatterns = router.urls
