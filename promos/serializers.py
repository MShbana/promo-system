from rest_framework import serializers

from .models import Promo


class PromoAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = '__all__'
