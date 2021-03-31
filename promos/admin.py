from django.contrib import admin

from . import models


class PromoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'normal_user',
        'promo_code',
        'is_active',
        'promo_type',
        'promo_amount',
        'description',
        'creation_time',
        'start_time',
        'end_time',
    ]
    raw_id_fields = [
        'normal_user',
    ]


admin.site.register(models.Promo, PromoAdmin)