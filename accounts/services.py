from . import models


def create_user(validated_data, is_staff=False, is_superuser=False):
    """
    Create Auth User.
    """
    user = models.User(
        username=validated_data['username'],
        name=validated_data['name'],
    )
    user.set_password(validated_data['password'])
    user.is_staff = is_staff
    user.is_superuser = is_superuser
    user.save()
    return user


def create_admin_user(validated_data):
    """
    Create Administrator User, and relate it to the created auth user object.
    """
    user = create_user(validated_data, is_staff=True, is_superuser=True)
    models.AdministratorUser.objects.create(
        user=user,
        address=validated_data['address']
    )
    return user

def create_normal_user(validated_data):
    """
    Create Administrator User, and relate it to the created auth user object.
    """

    user = create_user(validated_data, is_staff=False, is_superuser=False)
    models.NormalUser.objects.create(
        user=user,
        address=validated_data['address'],
        mobile_number=validated_data['mobile_number']
    )
    return user