from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import (
    Promo
)
from .permissions import (
    IsNormalUserAndOwner
)
from .serializers import(
    PromoAdminUserSerializer,
    PromoNormalUserSerializerList,
    PromoNormalUserSerializerRetreive
)
from .services import (
    DeductPromoAmount
)


class PromoAdminUser(viewsets.ModelViewSet):
    """
    Provide CREATE, READ, UPDATE & DELETE methods for admin users on promos.
    The token used to call this API must be an admin user's token.
    """
    permission_classes = [IsAdminUser,]
    serializer_class = PromoAdminUserSerializer
    queryset = Promo.objects.all()


class PromoNormalUser(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet
    ):
    """
    Provide CREATE, READ, UPDATE (only amount) methods for a normal users on their own promos.
    The token used to call this API must be a normal user's token (the owner of the promo).
    """
    permission_classes = [IsAuthenticated, IsNormalUserAndOwner]
    serializer_class = PromoNormalUserSerializerList

    def get_queryset(self):
        return Promo.objects.filter(
            normal_user=self.request.user.normaluser,
            is_active=True
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return PromoNormalUserSerializerList
        return PromoNormalUserSerializerRetreive

    def update(self, request, *args, **kwargs):
        promo = self.get_object()
        amt_to_deduct = request.data.get('amt_to_deduct')

        deduction_service_obj = DeductPromoAmount(promo, amt_to_deduct)
        if not deduction_service_obj.is_successful_deduction():
            return Response(
                {'error': deduction_service_obj.get_failure_message()},
                status=status.HTTP_400_BAD_REQUEST
            )

        deduction_service_obj.deduct_promo_amt()
        serializer = self.get_serializer(promo)
        return Response(serializer.data, status=status.HTTP_200_OK)
