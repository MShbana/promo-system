from rest_framework import serializers

from .models import Promo


class PromoAdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = '__all__'


class PromoNormalUserSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Promo
        exclude = [
            'normal_user',
            'creation_time',
            'is_active',
        ]


class PromoNormalUserSerializerRetreive(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = [
            'promo_code',
            'promo_amount'
        ]

