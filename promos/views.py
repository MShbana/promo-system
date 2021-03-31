from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from . import models, serializers


class PromoAdmin(viewsets.ModelViewSet):
    """
    Provide CREATE, READ, UPDATE & DELETE methods for admin users on promos.
    The token used to call this API must be an admin user's token.
    """

    permission_classes = [IsAdminUser,]
    serializer_class = serializers.PromoAdminSerializer
    queryset = models.Promo.objects.all()
