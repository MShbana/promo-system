from django.db import models


class Promo(models.Model):
    normal_user = models.ForeignKey(
        'accounts.NormalUser',
        on_delete=models.CASCADE
    )
    promo_code = models.CharField(
        unique=True,
        max_length=50
    )
    promo_type = models.CharField(
        max_length=255
    )
    promo_amount = models.PositiveIntegerField(
    )
    description = models.TextField(
    )
    creation_time = models.DateTimeField(
        auto_now_add=True
    )
    start_time = models.DateTimeField(
    )
    end_time = models.DateTimeField(
    )
    is_active = models.BooleanField(
        default=True
    )


    def __str__(self):
        return self.promo_code
