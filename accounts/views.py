from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from .serializers import (
    RegisterAdminUserSerializer,
    RegisterNormalUserSerializer
)


class RegisterAdminUser(APIView):
    """
    Register admin user.
    """
    permission_classes = [HasAPIKey, ]

    def post(self, request, format=None):
        serializer = RegisterAdminUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegisterNormalUser(APIView):
    """
    Register normal user.
    """
    permission_classes = [AllowAny, ]

    def post(self, request, format=None):
        serializer = RegisterNormalUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
