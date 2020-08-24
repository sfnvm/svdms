import logging
from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import status

from django.http import JsonResponse
from django.forms.models import model_to_dict

from django_filters import rest_framework as filters

from orders.models import (
    RequestOrder as RequestOrderModel,
    AgreedOrder as AgreedOrderModel
)

from orders.serializers import (
    RequestOrderSerializer,
    RequestOrderProductDetailsSerializer,
    AgreedOrderSerializer,
    AgreedOrderProductDetailsSerializer
)

User = get_user_model()
logger = logging.getLogger(__name__)


class RequestOrderFilter(filters.FilterSet):
    f_created_at = filters.DateTimeFilter(
        field_name="created_at", lookup_expr='gte')
    t_created_at = filters.DateTimeFilter(
        field_name="created_at", lookup_expr='lte')

    class Meta:
        model = RequestOrderModel
        fields = {
            'agency': ['exact'],
            'approved': ['exact']
        }


class RequestOrderViewSet(ModelViewSet):
    queryset = RequestOrderModel.objects.all().order_by(
        'created_at').filter(removed=False)
    serializer_class = RequestOrderSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, )
    filterset_class = RequestOrderFilter
    search_fields = ['code']

    def auto_create_agreed_order(self, data):
        print('approved')

    def perform_create(self, serializer):
        req = serializer.context['request']
        req_data = serializer.validated_data
        if "approved" in req_data:
            if req_data['approved']:
                self.auto_create_agreed_order(req_data)
        serializer.save(created_by=req.user)

    def perform_update(self, serializer):
        instance = serializer.save()

    @action(detail=True, methods=['put'])
    def confirm(self, request, pk=None):
        req_order = RequestOrderModel.objects.filter(pk=pk).first()
        if(not req_order.approved):
            queryset = RequestOrderModel.objects.filter(pk=pk)
            serialzer = RequestOrderSerializer(queryset)
            result = serialzer.approving(request.user, queryset.first())
            return Response(RequestOrderSerializer(result).data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AgreedOrderFilter(filters.FilterSet):
    class Meta:
        model = AgreedOrderModel
        fields = {
            'accepted': ['exact'],
            'rejected': ['exact'],
            'approved': ['exact'],
            'planned_for_delivery': ['exact'],
            'delivered': ['exact'],
            'paid': ['exact'],
        }


class AgreedOrderViewSet(ModelViewSet):
    queryset = AgreedOrderModel.objects.all().order_by(
        'created_at').filter(removed=False)
    serializer_class = AgreedOrderSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, )
    filterset_class = AgreedOrderFilter
    search_fields = ['code']

    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user)
