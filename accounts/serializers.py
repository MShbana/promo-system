from rest_framework import serializers
from rest_framework.authtoken.models import Token

from . import models, services


class RegisterAdminSerializerGet(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = [
            'username',
            'name',
            'address',
            'auth_token'
        ]

    def get_address(self, obj):
        return obj.administratoruser.address
    
    def get_auth_token(self, obj):
        return Token.objects.get(user=obj)


class RegisterAdminSerializerPost(serializers.ModelSerializer):
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
        model = models.User
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


    def to_representation(self, instance):
        """
        Return a custom response from the RegisterAdminSerializerGet.
        """
        return RegisterAdminSerializerGet(instance).data

    def create(self, validated_data):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match.'}
            )
        user = services.create_admin_user(self.validated_data)

        return user

