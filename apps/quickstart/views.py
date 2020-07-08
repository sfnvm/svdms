from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from apps.quickstart.models import (
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
    # TEST API VIEWSET
    # def get(self, request, format=None):
    #     user_count = User.objects.filter(is_active=True).count()
    #     content = {'user_count': user_count}
    #     return Response({
    #         'details': 'Thành công',
    #         'result': content
    #     })
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


###############
##### OTP #####
###############


###########################
##### Other Endpoints #####
###########################

class AgencyViewSet(ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductTypeViewSet(ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer


class MasterProductPriceViewSet(ModelViewSet):
    queryset = MasterProductPrice.objects.all()
    serializer_class = MasterProductPriceSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class StorageViewSet(ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
