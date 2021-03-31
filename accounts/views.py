from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers


class RegisterAdminUser(APIView):
    def post(self, request, format=None):
        serializer = serializers.RegisterAdminSerializerPost(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
