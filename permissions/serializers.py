from rest_framework import serializers
from django.contrib.auth.models import (
    Group,
    Permission
)


class GroupSerializer(serializers.ModelSerializer):  # OK no need it yet
    class Meta:
        model = Group
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):  # OK no need it yet
    class Meta:
        model = Permission
        fields = '__all__'
