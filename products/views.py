import logging
from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from products.models import (
    Product as ProductModel,
    ProductType as ProductTypeModel,
    ProductUnitType as ProductUnitTypeModel,
    MasterProductPrice as MasterProductPriceModel
)

from products.serializers import (
    ProductSerializer,
    ProductTypeSerializer,
    ProductUnitTypeSerializer,
    MasterProductPriceSerializer
)

User = get_user_model()
logger = logging.getLogger(__name__)


class ProductTypeViewSet(ModelViewSet):
    queryset = ProductTypeModel.objects.all().order_by('id').filter(removed=False)
    serializer_class = ProductTypeSerializer

    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user)

    def perform_destroy(self, request):
        instance.delete()


class ProductUnitPyteViewSet(ModelViewSet):
    queryset = ProductUnitTypeModel.objects.all().order_by(
        'id').filter(removed=False)
    serializer_class = ProductUnitTypeSerializer

    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user)

    def perform_destroy(self, request):
        instance.delete()


class ProductViewSet(ModelViewSet):
    queryset = ProductModel.objects.all().order_by('id').filter(removed=False)
    serializer_class = ProductSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user)

    def perform_destroy(self, request):
        instance.delete()


class MasterProductPriceViewSet(ModelViewSet):
    queryset = MasterProductPriceModel.objects.all().order_by(
        'id').filter(removed=False)
    serializer_class = MasterProductPriceSerializer

    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user)

    def perform_destroy(self, request):
        instance.delete()
