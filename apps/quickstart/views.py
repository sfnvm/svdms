from django.shortcuts import render
from django.contrib.auth.models import User, Group, Permission
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from rest_framework.permissions import DjangoModelPermissions

from apps.quickstart.models import (
    Profile,
    Agency,
    Product,
    ProductType,
    MasterProductPrice,
    Order,
    Storage
)

from apps.quickstart.serializers import (
    UserSerializer,
    GroupSerializer,
    PermissionSerializer,
    ProfileSerializer,
    AgencySerializer,
    ProductSerializer,
    ProductTypeSerializer,
    MasterProductPriceSerializer,
    OrderSerializer,
    StorageSerializer
)


#####################
##### User Auth #####
#####################

class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerializer

class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all().order_by('id')
    serializer_class = PermissionSerializer


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all().order_by('id')
    serializer_class = ProfileSerializer


###############
##### OTP #####
###############


###########################
##### Other Endpoints #####
###########################

class AgencyViewSet(ModelViewSet):
    queryset = Agency.objects.all().order_by('id')
    serializer_class = AgencySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer


class ProductTypeViewSet(ModelViewSet):
    queryset = ProductType.objects.all().order_by('id')
    serializer_class = ProductTypeSerializer


class MasterProductPriceViewSet(ModelViewSet):
    queryset = MasterProductPrice.objects.all().order_by('id')
    serializer_class = MasterProductPriceSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer


class StorageViewSet(ModelViewSet):
    queryset = Storage.objects.all().order_by('id')
    serializer_class = StorageSerializer
