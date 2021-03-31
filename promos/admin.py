from django.contrib import admin

from . import models


class PromoAdmin(admin.ModelAdmin):
    list_display = [
        'normal_user',
        'promo_code',
        'promo_type',
        'promo_amount',
        'description',
        'creation_time',
        'start_time',
        'end_time',
        'is_active',
    ]
    raw_id_fields = [
        'normal_user',
    ]


admin.site.register(models.Promo, PromoAdmin)