import logging
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils import timezone

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

from agencies.models import (
    Agency as AgencyModel
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
            'approved': ['exact'],
            'rejected': ['exact']
        }


class RequestOrderViewSet(ModelViewSet):
    queryset = RequestOrderModel.objects.all().order_by(
        '-created_at').filter(removed=False)
    queryset = RequestOrderSerializer.setup_eager_loading(queryset)
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
        req = serializer.context['request']
        instance = serializer.save(created_by=req.user)

    @action(detail=True, methods=['put'])
    def confirm(self, request, pk=None):
        req_order = RequestOrderModel.objects.filter(pk=pk).first()
        if(not req_order.approved):
            queryset = RequestOrderModel.objects.filter(pk=pk)
            serializer = RequestOrderSerializer(queryset)
            result = serializer.approving(request.user, queryset.first())
            return Response(RequestOrderSerializer(result).data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def reject(self, request, pk=None):
        req_order = RequestOrderModel.objects.filter(pk=pk).first()
        if req_order.approved or req_order.rejected:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            req_order.rejected = True
            req_order.save()
            queryset = RequestOrderModel.objects.filter(pk=pk).first()
            return Response(RequestOrderSerializer(queryset).data)


class AgreedOrderFilter(filters.FilterSet):
    class Meta:
        model = AgreedOrderModel
        fields = {
            'paid': ['exact'],
            'status': ['exact'],
            'request_order': ['exact']
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

    @action(detail=False)
    def current_agency(self, request):
        agency_instance = AgencyModel.objects.filter(
            user_related=request.user).first()
        if(not agency_instance):
            return Response(data={
                'details': 'permission denied'
            }, status=status.HTTP_400_BAD_REQUEST)

        ago_orders = AgreedOrderModel.objects.filter(
            status=0, agency=agency_instance).order_by('created_at')

        page = self.paginate_queryset(ago_orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(ago_orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def paid_confirm(self, request, pk=None):
        ago_order = AgreedOrderModel.objects.filter(
            pk=pk, status=11).first()

        if(not ago_order):
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"details": "not found"}
            )

        ago_order.paid = True
        ago_order.paid_on = timezone.now()
        ago_order.confirm_paid_by = request.user
        ago_order.save()

        serializer = self.get_serializer(ago_order, many=False)
        return Response(data={serializer.data})

    @action(detail=True, methods=['put'])
    def agency_accept(self, request, pk=None):
        agency_instance = AgencyModel.objects.filter(
            user_related=request.user).first()
        ago_order = AgreedOrderModel.objects.filter(
            pk=pk, status=0, agency=agency_instance).order_by('created_at').first()

        if(not ago_order):
            return Response(status=status.HTTP_404_NOT_FOUND)

        ago_order.agency_accepted = True
        ago_order.agency_accepted_on = timezone.now()
        ago_order.status = 11
        ago_order.save()

        serializer = self.get_serializer(ago_order, many=False)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def agency_reject(self, request, pk=None):
        agency_instance = AgencyModel.objects.filter(
            user_related=request.user).first()
        ago_order = AgreedOrderModel.objects.filter(
            pk=pk, status=0, agency=agency_instance).first()

        if(not ago_order):
            return Response(status=status.HTTP_404_NOT_FOUND)

        ago_order.agency_rejected = True
        ago_order.agency_rejected_on = timezone.now()
        ago_order.status = 10
        ago_order.save()

        serializer = self.get_serializer(ago_order, many=False)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def approve(self, request):
        print(request)

    @action(detail=True, methods=['put'])
    def reject(self, request):
        print(request)

    @action(detail=True, methods=['put'])
    def plant_for_delivery(self, request, pk=None):
        ago_order = AgreedOrderModel.objects.filter(
            pk=pk, status=11).first()

        if(not ago_order):
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"details": "not found"}
            )

        ago_order.planned_for_delivery = True
        ago_order.expected_delivery_on = request.data['timestamp']
        ago_order.status = 33
        ago_order.save()

        serializer = self.get_serializer(ago_order, many=False)
        return Response(data={serializer.data})

    @action(detail=True, methods=['put'])
    def delivered(self, request, pk=None):
        ago_order = AgreedOrderModel.objects.filter(
            pk=pk, status=33).first()

        if(not ago_order):
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"details": "not found"}
            )

        ago_order.delivered = True
        ago_order.delivered_on = request.data['timestamp']
        ago_order.status = 44
        ago_order.save()

        serializer = self.get_serializer(ago_order, many=False)
        return Response(data={serializer.data})
