from .models import (
    AdministratorUser,
    NormalUser,
    User
)


class RegisterUserBase:
    """
    Base class, inherited by both RegisterAdminUser & RegisterNormalUser classes.
    """
    def __init__(self, validated_data):
        self.validated_data = validated_data

    def do_passwords_match(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        return password == password2

    def existing_user_name(self):
        username = self.validated_data['username']

        # Make sure username filteration is case insensitive to prevent duplicated.
        return User.objects.filter(username__iexact=username).exists()


class RegisterAdminUser(RegisterUserBase):
    def create_admin_user(self):
        """
        Create Administrator User, and relate it to the created auth user object.
        """
        user = User.objects.create_superuser(
            username=self.validated_data['username'],
            name=self.validated_data['name'],
            password=self.validated_data['password']
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
        user = User.objects.create_superuser(
            username=self.validated_data['username'],
            name=self.validated_data['name'],
            password=self.validated_data['password']
        )
        NormalUser.objects.create(
            user=user,
            address=self.validated_data['address'],
            mobile_number=self.validated_data['mobile_number']
        )
        return user
