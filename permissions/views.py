from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from django.contrib.auth.models import (
    Group,
    Permission
)

from permissions.serializers import (
    GroupSerializer,
    PermissionSerializer
)


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerializer


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all().order_by('id')
    serializer_class = PermissionSerializer
