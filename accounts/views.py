from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


from . import serializers


class RegisterAdminUser(APIView):
    def post(self, request, format=None):
        serializer = serializers.RegisterAdminSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            administrator_user = user.administratoruser
            return Response(
                {
                    'username': user.username,
                    'name': user.name,
                    'address': administrator_user.address,
                    'auth_token': Token.objects.get(user=user).key
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)