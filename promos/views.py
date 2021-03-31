from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from . import models, serializers


class PromoAdmin(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication,]

    permission_classes = [IsAdminUser,]

    def list(self, request):
        queryset = models.Promo.objects.all()
        serializer = serializers.PromoAdminSerializer(queryset, many=True)
        return Response(serializer.data)


    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
