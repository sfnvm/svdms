from django.contrib.auth.models import (
    Group,
    Permission
)
from rest_framework import serializers

from quickstart import models as app_models


#------------------#
# USER AND PROFILE #
#------------------#
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

        profile_instance = app_models.Profile.objects.filter(user=user)

        if(profile_instance):
            profile_instance.update(**profile_data)
        else:
            app_models.Profile.objects.create(user=user, **profile_data)

        return user


#-----------------------#
# GROUP AND PERMISSIONS #
#-----------------------#
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


#--------#
# AGENCY #
#--------#
class AgencySerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True)

    def validate_user(self, value):
        return self.context['request'].user

    class Meta:
        model = app_models.Agency
        fields = '__all__'


#----------------------#
# PRODUCTS AND PRICING #
#----------------------#
class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = app_models.ProductType
        fields = '__all__'


class ProductUnitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = app_models.ProductUnitType
        fields = '__all__'


class MasterProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = app_models.MasterProductPrice
        fields = '__all__'


# Need separate list vs create, update. This way ok by now
class ProductSerializer(serializers.ModelSerializer):
    # product_type = ProductTypeSerializer()
    # product_unit_type = ProductUnitTypeSerializer()

    class Meta:
        model = app_models.Product
        fields = '__all__'


#----------------------#
# ORDERS AND AGREEMENT #
#----------------------#
class RequestOrderProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = app_models.RequestOrderProductDetails
        fields = '__all__'


class AgreedOrderProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = app_models.AgreedOrderProductDetails
        fields = '__all__'


class RequestOrderSerializer(serializers.ModelSerializer):
    details = serializers.ListField(RequestOrderProductDetailsSerializer())

    class Meta:
        model = app_models.RequestOrder
        fields = '__all__'

    def create(self, validated_data):
        request_order_data = validated_data.pop('details')

        request_order = app_models.RequestOrder.objects.create(
            **validated_data)

        for req_order in request_order_data:
            app_models.RequestOrderProductDetails.objects.create(
                request_oder, **req_order)

        return request_order

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')

        req = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()

        profile_instance = app_models.Profile.objects.filter(user=user)

        if(profile_instance):
            profile_instance.update(**profile_data)
        else:
            app_models.Profile.objects.create(user=user, **profile_data)

        return user


class AgreedOrderSerializer(serializers.ModelSerializer):
    details = AgreedOrderProductDetailsSerializer()

    class Meta:
        model = app_models.AgreedOrder
        fields = '__all__'


#---------#
# STORAGE #
#---------#
class StorageProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = app_models.StorageProductDetails
        fields = '__all__'


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = app_models.Storage
        fields = '__all__'
