from rest_framework import serializers
from areas.models import (
    Area,
    AreaSalesmanDetails,
    AreaAgencyDetails
)
from users.models import User
from users.serializers import UserSerializer
from agencies.models import Agency
from agencies.serializers import AgencySerializer


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class AreaSalesmanSerializer(serializers.ModelSerializer):
    area = AreaSerializer(read_only=True)
    area_id = serializers.PrimaryKeyRelatedField(
        source='area', write_only=True,
        queryset=Area.objects.order_by('id'))

    salesman = UserSerializer(read_only=True)
    salesman_id = serializers.PrimaryKeyRelatedField(
        source='salesman', write_only=True,
        queryset=User.objects.order_by('id'))

    class Meta:
        model = AreaSalesmanDetails
        fields = '__all__'


class AreaAgencySerializer(serializers.ModelSerializer):
    area = AreaSerializer(read_only=True)
    area_id = serializers.PrimaryKeyRelatedField(
        source='area', write_only=True,
        queryset=Area.objects.order_by('id'))

    agency = AgencySerializer(read_only=True)
    agency_id = serializers.PrimaryKeyRelatedField(
        source='agency', write_only=True,
        queryset=Agency.objects.order_by('id'))

    class Meta:
        model = AreaAgencyDetails
        fields = '__all__'
