from django.contrib.auth.models import (
    User,
    Group
)
from rest_framework.serializers import HyperlinkedModelSerializer

from apps.quickstart.models import (
    Agency,
    ProductType,
    ProductUnitType,
    Product,
)


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class AgencySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Agency
        fields = ['code', 'name', 'address', 'phone_number', 'created_at']


class ProductTypeSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ProductType,
        fields = ['added_by', 'code', 'unit_type', 'removed']