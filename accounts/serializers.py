from rest_framework import serializers
from . import models


class RegisterAdminSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
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

    def create(self, validated_data):
        user = models.User(
            username=validated_data['username'],
            name=self.validated_data['name'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match.'}
            )
        user.set_password(validated_data['password'])
        user.is_staff = True
        user.is_superuser = True
        user.save()

        models.AdministratorUser.objects.create(
            user=user,
            address=self.validated_data['address']
        )
        return user