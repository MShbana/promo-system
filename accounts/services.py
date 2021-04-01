from .models import (
    AdministratorUser,
    NormalUser,
    User
)


class RegisterUserBase():
    def __init__(self, validated_data):
        self.validated_data = validated_data

    def do_passwords_match(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        return password == password2

    def existing_user_name(self):
        username = self.validated_data['username']
        return User.objects.filter(username__iexact=username).exists()

    def create_user(self, is_staff=False, is_superuser=False):
        """
        Create Auth User.
        """
        user = User.objects.create_user(
            username=self.validated_data['username'],
            name=self.validated_data['name'],
            password=self.validated_data['password'],
            is_staff=is_staff,
            is_superuser=is_superuser
        )
        return user


class RegisterAdminUser(RegisterUserBase):
    def create_admin_user(self):
        """
        Create Administrator User, and relate it to the created auth user object.
        """
        user = self.create_user(
            is_staff=True,
            is_superuser=True
        )
        AdministratorUser.objects.create(
            user=user,
            address=self.validated_data['address']
        )
        return user


class RegisterNormalUser(RegisterUserBase):
    def create_normal_user(self):
        """
        Create Administrator User, and relate it to the created auth user object.
        """
        user = self.create_user()
        NormalUser.objects.create(
            user=user,
            address=self.validated_data['address'],
            mobile_number=self.validated_data['mobile_number']
        )
        return user
