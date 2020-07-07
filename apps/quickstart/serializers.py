from django.contrib.auth.models import (
    User,
    Group
)
from rest_framework import serializers

from apps.quickstart.models import (
    Profile,
    Agency,
    ProductType,
    ProductUnitType,
    Product,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'first_name', 'last_name', 'groups']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data('first_name', instance.first_name)
        instance.last_name = validated_data('last_name', instance.last_name)
        instance.groups = validated_data('groups', instance.groups)

        instance.save()
        return instance

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = []
        

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class AgencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Agency
        fields = ['code', 'name', 'address', 'phone_number', 'created_at']


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductType,
        fields = ['added_by', 'code', 'unit_type', 'removed']