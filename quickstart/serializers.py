import logging
from datetime import datetime, date

from django.contrib.auth.models import (
    Group,
    Permission
)
from django.db.models import Sum

from rest_framework import serializers

from quickstart import models as app_models


# Libs instance
logger = logging.getLogger(__name__)


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
        extra_kwargs = {
            'password': {'write_only': True}
        }

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
class GroupSerializer(serializers.ModelSerializer):  # OK no need it yet
    class Meta:
        model = Group
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):  # OK no need it yet
    class Meta:
        model = Permission
        fields = '__all__'


#--------#
# AGENCY #
#--------#
class AgencySerializer(serializers.ModelSerializer):  # OK
    created_by = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        model = app_models.Agency
        fields = '__all__'


#----------------------#
# PRODUCTS AND PRICING #
#----------------------#
class ProductTypeSerializer(serializers.ModelSerializer):  # OK
    class Meta:
        model = app_models.ProductType
        fields = '__all__'


class ProductUnitTypeSerializer(serializers.ModelSerializer):  # OK
    class Meta:
        model = app_models.ProductUnitType
        fields = '__all__'


class MasterProductPriceSerializer(serializers.ModelSerializer):  # OK
    class Meta:
        model = app_models.MasterProductPrice
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):  # OK
    product_type = ProductTypeSerializer(read_only=True)
    product_type_id = serializers.PrimaryKeyRelatedField(
        source='product_type', queryset=app_models.ProductType.objects.order_by('id').filter(removed=False), write_only=True)

    product_unit_type = ProductUnitTypeSerializer(read_only=True)
    product_unit_type_id = serializers.PrimaryKeyRelatedField(
        source='product_unit_type', queryset=app_models.ProductUnitType.objects.order_by('id').filter(removed=False), write_only=True)

    current_price = serializers.SerializerMethodField()
    available_quantity = serializers.SerializerMethodField()

    def get_current_price(self, obj):
        master_price = app_models.MasterProductPrice.objects.filter(
            product=obj, removed=False).order_by('created_at').reverse()
        for mprice in master_price:
            if mprice.from_date > date.today():
                continue
            if mprice.to_date >= date.today():
                return mprice.price

        return obj.base_price

    def get_available_quantity(self, obj):
        all_input = app_models.StorageProductDetails.objects.filter(
            product=obj).aggregate(all_input=Sum('amount'))['all_input'] or 0

        current_sold = app_models.AgreedOrder.objects.filter(
            delivered=True, paid=True)

        soldSum = 0
        for success_order in current_sold:
            tmp = app_models.AgreedOrderProductDetails.objects.filter(
                agreed_order=success_order).aggregate(tmp=Sum('amount'))['tmp'] or 0
            if tmp:
                soldSum += tmp

        return all_input - soldSum

    # get price at current time
    def __init__(self, *args, **kwargs):
        super(ProductSerializer, self).__init__(*args, **kwargs)

        try:
            if self.context['request'].method == 'GET':
                pass
        except KeyError:
            pass

    class Meta:
        model = app_models.Product
        fields = '__all__'


#----------------------#
# ORDERS AND AGREEMENT #
#----------------------#
class RequestOrderProductDetailsSerializer(serializers.ModelSerializer):  # OK
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        source='product', queryset=app_models.Product.objects.order_by('id').filter(removed=False), write_only=True)

    class Meta:
        model = app_models.RequestOrderProductDetails
        exclude = ['request_order']


class AgreedOrderProductDetailsSerializer(serializers.ModelSerializer):  # OK
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        source='product', queryset=app_models.Product.objects.order_by('id').filter(removed=False), write_only=True)

    class Meta:
        model = app_models.AgreedOrderProductDetails
        fields = '__all__'


class RequestOrderSerializer(serializers.ModelSerializer):  # OK
    created_by = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True
    )

    agency = AgencySerializer(read_only=True)
    agency_id = serializers.PrimaryKeyRelatedField(
        source='agency', queryset=app_models.Agency.objects.order_by('id').filter(removed=False), write_only=True)

    requestorderproductdetails_set = RequestOrderProductDetailsSerializer(
        many=True, read_only=True)
    details = serializers.JSONField(write_only=True)

    class Meta:
        model = app_models.RequestOrder
        fields = '__all__'
        read_only_fields = ['bill_value']

    def create(self, validated_data):
        request_order_data = validated_data.pop('details')

        request_order = app_models.RequestOrder.objects.create(
            **validated_data)

        for req_order in request_order_data:
            app_models.RequestOrderProductDetails.objects.create(
                request_order=request_order, **req_order)

        return request_order

    def update(self, instance, validated_data):
        request_order_data = validated_data.pop('details')

        instance.__dict__.update(**validated_data)
        instance.save()

        app_models.RequestOrderProductDetails.objects.filter(
            request_order=instance).delete()

        # TODO 500
        for req_order in request_order_data:
            app_models.RequestOrderProductDetails.objects.create(
                request_order=instance, **req_order)

        return instance


class AgreedOrderSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True)

    agency = AgencySerializer(read_only=True)
    agency_id = serializers.PrimaryKeyRelatedField(
        source='agency', queryset=app_models.Agency.objects.order_by('id').filter(removed=False), write_only=True)

    requestorderproductdetails_set = RequestOrderProductDetailsSerializer(
        many=True, read_only=True)
    details = serializers.JSONField(
        write_only=True)

    class Meta:
        model = app_models.AgreedOrder
        fields = '__all__'

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


#---------#
# STORAGE #
#---------#
class StorageProductDetailsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        source='product', queryset=app_models.Product.objects.order_by('id').filter(removed=False), write_only=True)

    class Meta:
        model = app_models.StorageProductDetails
        fields = '__all__'


class StorageSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True)

    storageproductdetails_set = StorageProductDetailsSerializer(
        many=True, read_only=True)
    details = serializers.JSONField(
        write_only=True)

    class Meta:
        model = app_models.Storage
        fields = '__all__'

    def create(self, validated_data):
        storage_data = validated_data.pop('details')

        storage = app_models.Storage.objects.create(
            **validated_data)

        for data in storage_data:
            app_models.StorageProductDetails.objects.create(
                storage=storage, **data)

        return storage

    def update(self, instance, validated_data):
        storage_data = validated_data.pop('details')

        instance.__dict__.update(**validated_data)
        instance.save()

        app_models.StorageProductDetails.objects.filter(
            storage=instance).delete()

        for data in storage_data:
            app_models.StorageProductDetails.objects.create(
                request_order=instance, **data)

        return instance
