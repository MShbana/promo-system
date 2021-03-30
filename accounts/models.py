from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    class Types(models.TextChoices):
        ADMIN = 'ADMIN', 'ADMIN'
        NORMAL = 'NORMAL', 'NORMAL'

    username = models.CharField(
        max_length=255,
        unique=True
    )
    name = models.CharField(
        max_length=255
    )
    address = models.TextField(
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        default=True
    )
    is_staff = models.BooleanField(
        default=False
    )
    is_superuser = models.BooleanField(
        default=False
    )

    type = models.CharField(
        max_length=6,
        choices=Types.choices,
        default=Types.NORMAL
    )

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['name', ]

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
