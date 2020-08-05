from rest_framework import serializers
from rest_framework import filters

from products.models import (
    Product as ProductModel
)
from storages.models import (
    Storage as StorageModel,
    StorageProductDetails as StorageProductDetailsModel
)

from products.serializers import ProductSerializer


class StorageProductDetailsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        source='product', write_only=True,
        queryset=ProductModel.objects.order_by('id').filter(removed=False))

    model = StorageProductDetailsModel

    class Meta:
        fields = '__all__'


class StorageSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True)

    storageproductdetails_set = StorageProductDetailsSerializer(
        many=True, read_only=True)
    details = serializers.JSONField(
        write_only=True)

    class Meta:
        model = StorageModel
        fields = '__all__'

    def create(self, validated_data):
        storage_data = validated_data.pop('details')

        storage = StorageModel.objects.create(
            **validated_data)

        for data in storage_data:
            StorageProductDetailsModel.objects.create(
                storage=storage, **data)

        return storage

    def update(self, instance, validated_data):
        storage_data = validated_data.pop('details')

        instance.__dict__.update(**validated_data)
        instance.save()

        StorageProductDetailsModel.objects.filter(
            storage=instance).delete()

        for data in storage_data:
            StorageProductDetailsModel.objects.create(
                request_order=instance, **data)

        return instance
