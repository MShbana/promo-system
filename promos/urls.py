from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register(r'promo-admin', views.PromoAdmin, basename='promo_admin')

urlpatterns = router.urls
