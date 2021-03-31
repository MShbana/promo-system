from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User
from .services import (
    create_admin_user,
    create_normal_user,
    do_passwords_match,
    existing_user_name
)


class CreateAuthUserSerializer(serializers.ModelSerializer):
    """
    Base class for creating the auth user.
    Inherited by both RegisterAdminUserSerializer & RegisterNormalUserSerializer
    The actual `create` and `to_representation` methods implementation (overriding)
    is done in each of the extended classes corresponding to the type of the registered user.
    """
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    # allow_null is discouraged by the rest framework docs,
    # allow_blank assures that address is sent for data consistency. 
    # In case the user didn't add an address, it should be address:"".
    address = serializers.CharField(
        allow_blank=True
    )

    class Meta:
        model = User
        fields = [
            'username',
            'name',
            'address',
            'password',
            'password2'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }


class GetAdminUserSerializer(serializers.ModelSerializer):
    """
    Used to customize the response in the admin user registeration endpoint;
    to return the extra fields that are related to the admin user only.
    Passed to `to_representation` method in RegisterAdminUserSerializer.
    """
    address = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'name',
            'address',
            'auth_token'
        ]

    def get_id(self, obj):
        return obj.administratoruser.id

    def get_address(self, obj):
        return obj.administratoruser.address
    
    def get_auth_token(self, obj):
        return Token.objects.get(user=obj)


class GetNormalUserSerializer(serializers.ModelSerializer):
    """
    Used to customize the response in the normal user registeration endpoint;
    to return the extra fields that are related to the normal user only.
    Passed to `to_representation` method in RegisterNormalUserSerializer.
    """
    address = serializers.SerializerMethodField()
    mobile_number = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'name',
            'mobile_number',
            'address',
            'auth_token'
        ]

    def get_id(self, obj):
        return obj.normaluser.id

    def get_address(self, obj):
        return obj.normaluser.address
    
    def get_mobile_number(self, obj):
        return obj.normaluser.mobile_number
    
    def get_auth_token(self, obj):
        return Token.objects.get(user=obj)

class RegisterAdminUserSerializer(CreateAuthUserSerializer):
    """
    The main admin registeration API serializer.
    """
    def create(self, validated_data):
        if not do_passwords_match(self.validated_data):
            raise serializers.ValidationError(
                {'password': ['passwords do not match.']}
            )
        if existing_user_name(self.validated_data):
            raise serializers.ValidationError(
                {'username': ['user with this username already exists.']}
            )

        user = create_admin_user(self.validated_data)
        return user

    def to_representation(self, instance):
        """
        Return a custom response from the GetAdminUserSerializer.
        """
        return GetAdminUserSerializer(instance).data


class RegisterNormalUserSerializer(CreateAuthUserSerializer):
    """
    The main admin registeration API serializer.
    """

    mobile_number = serializers.CharField(
        max_length=15
    )
    class Meta(CreateAuthUserSerializer.Meta):
        fields = CreateAuthUserSerializer.Meta.fields + ['mobile_number',]

    def create(self, validated_data):
        if not do_passwords_match(self.validated_data):
            raise serializers.ValidationError(
                {'password': ['passwords do not match.']}
            )
        if existing_user_name(self.validated_data):
            raise serializers.ValidationError(
                {'username': ['user with this username already exists..']}
            )

        user = create_normal_user(self.validated_data)
        return user

    def to_representation(self, instance):
        """
        Return a custom response from the GetNormalUserSerializer.
        """
        return GetNormalUserSerializer(instance).data
