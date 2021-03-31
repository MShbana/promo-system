from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers


class RegisterAdminUser(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, format=None):
        serializer = serializers.RegisterAdminUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegisterNormalUser(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, format=None):
        serializer = serializers.RegisterNormalUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
