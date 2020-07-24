from django.shortcuts import render
from django.contrib.auth.models import User, Group, Permission
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import permissions

# Somewhat easy to use
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.permissions import DjangoModelPermissions

from quickstart import models as app_models
from quickstart import serializers as app_serializers


@api_view
def check_token(request):
    """
    Check token
    """
    if request.method == 'POST':
        content = {'details': 'Token is OK!'}
        return Response(content)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined').filter(is_active=True)
    serializer_class = app_serializers.UserSerializer
    # permission_classes = [permissions.IsAdminUser, ]


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all().order_by('id')
    serializer_class = app_serializers.GroupSerializer
    # permission_classes = [permissions.IsAdminUser, ]


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all().order_by('id')
    serializer_class = app_serializers.PermissionSerializer


class ProfileViewSet(ModelViewSet):
    queryset = app_models.Profile.objects.all().order_by('id')
    serializer_class = app_serializers.ProfileSerializer


class AgencyViewSet(ModelViewSet):
    queryset = app_models.Agency.objects.all().order_by('id').filter(removed=False)
    serializer_class = app_serializers.AgencySerializer

    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user)

    def perform_destroy(self, request):
        instance = self.get_object()
        instance.removed_by = self.request.user
        instance.removed = True
        instance.save()


class ProductViewSet(ModelViewSet):
    queryset = app_models.Product.objects.all().order_by('id').filter(removed=False)
    serializer_class = app_serializers.ProductSerializer


class ProductTypeViewSet(ModelViewSet):
    queryset = app_models.ProductType.objects.all().order_by('id').filter(removed=False)
    serializer_class = app_serializers.ProductTypeSerializer


class MasterProductPriceViewSet(ModelViewSet):
    queryset = app_models.MasterProductPrice.objects.all().order_by('id').filter(removed=False)
    serializer_class = app_serializers.MasterProductPriceSerializer


class RequestOrderViewSet(ModelViewSet):
    queryset = app_models.RequestOrder.objects.all().order_by('id').filter(removed=False)
    serializer_class = app_serializers.RequestOrderSerializer


class AgreedOrderViewSet(ModelViewSet):
    queryset = app_models.AgreedOrder.objects.all().order_by('id').filter(removed=False)
    serializer_class = app_serializers.AgreedOrderSerializer


class StorageViewSet(ModelViewSet):
    queryset = app_models.Storage.objects.all().order_by('id').filter(removed=False)
    serializer_class = app_serializers.StorageSerializer
