import logging
from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework import filters as ori_filter
from django_filters import rest_framework as drf_filter

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


class ProductTypeFilter(drf_filter.FilterSet):
    gte_created_at = drf_filter.DateTimeFilter(
        field_name="created_at", lookup_expr='gte')
    lte_created_at = drf_filter.DateTimeFilter(
        field_name="created_at", lookup_expr='lte')
    has_product = drf_filter.BooleanFilter(method='check_product_related')

    class Meta:
        model = ProductTypeModel
        fields = {
            'removed': ['exact']
        }

    def check_product_related(self, queryset, name, value):
        return queryset.filter(product__isnull=(not value)).distinct()


class ProductTypeViewSet(ModelViewSet):
    queryset = ProductTypeModel.objects.all().order_by('id')
    serializer_class = ProductTypeSerializer
    filter_backends = (drf_filter.DjangoFilterBackend,
                       ori_filter.SearchFilter, )
    filterset_class = ProductTypeFilter
    search_fields = ['code']

    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user)

    @action(detail=True, methods=['put'])
    def lock(self, request, pk=None):
        queryset = ProductTypeModel.objects.filter(pk=pk)
        queryset.update(removed=True, removed_by=request.user)
        serializer = ProductTypeSerializer(queryset, many=True)
        return Response(serializer.data[0])

    @action(detail=True, methods=['put'])
    def unlock(self, request, pk=None):
        queryset = ProductTypeModel.objects.filter(pk=pk)
        queryset.update(removed=False, removed_by=None)
        serializer = ProductTypeSerializer(queryset, many=True)
        return Response(serializer.data[0])


class ProductUnitTypeFilter(drf_filter.FilterSet):
    gte_created_at = drf_filter.DateTimeFilter(
        field_name="created_at", lookup_expr='gte')
    lte_created_at = drf_filter.DateTimeFilter(
        field_name="created_at", lookup_expr='lte')
    has_product = drf_filter.BooleanFilter(method='check_product_related')

    class Meta:
        model = ProductUnitTypeModel
        fields = {
            'removed': ['exact']
        }

    def check_product_related(self, queryset, name, value):
        return queryset.filter(product__isnull=(not value)).distinct()


class ProductUnitTypeViewSet(ModelViewSet):
    queryset = ProductUnitTypeModel.objects.all().order_by('id')
    serializer_class = ProductUnitTypeSerializer
    filter_backends = (drf_filter.DjangoFilterBackend,
                       ori_filter.SearchFilter, )
    filterset_class = ProductUnitTypeFilter
    search_fields = ['code']

    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user)

    @action(detail=True, methods=['put'])
    def lock(self, request, pk=None):
        queryset = ProductUnitTypeModel.objects.filter(pk=pk)
        queryset.update(removed=True, removed_by=request.user)
        serializer = ProductUnitTypeSerializer(queryset, many=True)
        return Response(serializer.data[0])

    @action(detail=True, methods=['put'])
    def unlock(self, request, pk=None):
        queryset = ProductUnitTypeModel.objects.filter(pk=pk)
        queryset.update(removed=False, removed_by=None)
        serializer = ProductUnitTypeSerializer(queryset, many=True)
        return Response(serializer.data[0])


class ProductFilter(drf_filter.FilterSet):
    gte_created_at = drf_filter.DateTimeFilter(
        field_name="created_at", lookup_expr='gte')
    lte_created_at = drf_filter.DateTimeFilter(
        field_name="created_at", lookup_expr='lte')

    class Meta:
        model = ProductModel
        fields = {
            'product_type': ['exact'],
            'product_unit_type': ['exact'],
            'code': ['exact']
        }


class ProductViewSet(ModelViewSet):
    queryset = ProductModel.objects.all().order_by('id').filter(removed=False)
    serializer_class = ProductSerializer

    filter_backends = (drf_filter.DjangoFilterBackend,
                       ori_filter.SearchFilter, )
    filterset_class = ProductFilter
    search_fields = ['name_latin', 'code']

    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user)


class MasterProductPriceViewSet(ModelViewSet):
    queryset = MasterProductPriceModel.objects.all().order_by(
        'id').filter(removed=False)
    serializer_class = MasterProductPriceSerializer

    filter_backends = (drf_filter.DjangoFilterBackend,
                       ori_filter.SearchFilter, )
    filterset_fields = {
        'product': ['exact'],
        'code': ['exact']
    }

    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user)
