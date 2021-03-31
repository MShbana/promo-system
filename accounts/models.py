from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

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
    date_joined = models.DateTimeField(
        auto_now_add=True
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


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Generate a token when a a new user object is created.
    """
    if created:
        Token.objects.create(user=instance)


class NormalUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    address = models.TextField(
        null=True,
        blank=True
    )
    mobile_number = models.CharField(
        max_length=15,
        null=True
    )

    def __str__(self):
        return self.user.username


class AdministratorUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    address = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username
