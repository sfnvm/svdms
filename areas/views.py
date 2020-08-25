from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from areas.models import (
    Area,
    AreaAgencyDetails,
    AreaSalesmanDetails
)
from areas.serializers import (
    AreaSerializer,
    AreaSalesmanSerializer,
    AreaAgencySerializer
)


class AreaViewSet(ModelViewSet):
    queryset = Area.objects.all().order_by('id')
    serializer_class = AreaSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, )
    search_fields = ['name_latin', 'code']


class AreaSalesmanViewSet(ModelViewSet):
    queryset = AreaSalesmanDetails.objects.all().order_by('id')
    serializer_class = AreaSalesmanSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, )
    filter_fields = ['salesman', 'area']


class AreaAgencyViewSet(ModelViewSet):
    queryset = AreaAgencyDetails.objects.all().order_by('id')
    serializer_class = AreaAgencySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, )
    filter_fields = ['agency', 'area']
