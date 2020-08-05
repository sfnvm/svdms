import logging
from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet

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

# Libs instance
User = get_user_model()
logger = logging.getLogger(__name__)


class RequestOrderViewSet(ModelViewSet):
    queryset = RequestOrderModel.objects.all().order_by('id').filter(removed=False)
    serializer_class = RequestOrderSerializer

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

    def perform_destroy(self, request):
        instance.delete()


class AgreedOrderViewSet(ModelViewSet):
    queryset = AgreedOrderModel.objects.all().order_by('id').filter(removed=False)
    serializer_class = AgreedOrderSerializer

    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user)

    def perform_destroy(self, request):
        instance.delete()
