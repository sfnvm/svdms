from quickstart import models as app_models
from django.contrib.auth.models import (
    User,
    Group,
    Permission
)
from rest_framework import serializers
from django.contrib.auth import get_user_model


class ProfileSerializer(serializers.ModelSerializer):  # OK
    class Meta:
        model = app_models.Profile
        exclude = ['user']


class UserSerializer(serializers.ModelSerializer):  # OK
    profile = ProfileSerializer()

    class Meta:
        model = app_models.User

        # Can't have 'fields' and 'exclude' at the same time
        fields = '__all__'
        read_only_fields = ('date_joined', 'is_superuser',
                            'is_staff', 'is_active')
        depth = 1
        # exclude = ['password']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')

        user = app_models.User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        app_models.Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')

        user = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()

        Profile.objects.filter(user=user).update(**profile_data)

        return user


# # OK // required admin permission please
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at',)


# OK // required admin permission please
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class AgencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = app_models.Agency
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = app_models.Product
        fields = '__all__'


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = app_models.ProductType
        fields = '__all__'


class MasterProductPriceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = app_models.MasterProductPrice
        fields = '__all__'


class RequestOrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = app_models.RequestOrder
        fields = '__all__'


class StorageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = app_models.Storage
        fields = '__all__'
