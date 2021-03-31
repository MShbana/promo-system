from django.contrib.auth.models import BaseUserManager

from . import models


class UserManager(BaseUserManager):
    def create_user(self, username, name, password=None, is_active=True, is_staff=False, is_superuser=False):
        if not username:
            raise ValueError('User must have a username.')

        if not password:
            raise ValueError('User must have a password.')

        if not name:
            raise ValueError('User must have a name.')

        user = self.model(
            username=self.model.normalize_username(username)
        )

        user.set_password(password)
        user.name = name
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser

        user.save(using=self._db)

        return user

    def create_staffuser(self, username, name, password=None):
        user = self.create_user(
            username,
            name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, username, name, password=None):
        user = self.create_user(
            username,
            name,
            password=password,
            is_staff=True,
            is_superuser=True
        )

        return user
        