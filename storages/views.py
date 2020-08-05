import logging
from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet

from storages.models import Storage as StorageModel

from storages.serializers import StorageSerializer

# Libs instance
User = get_user_model()
logger = logging.getLogger(__name__)


class StorageViewSet(ModelViewSet):
    queryset = StorageModel.objects.all().order_by('id').filter(removed=False)
    serializer_class = StorageSerializer

    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user)

    def perform_destroy(self, request):
        instance.delete()
