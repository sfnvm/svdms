from rest_framework import serializers
from django.db.models import Sum

from products.models import (
    Product as ProductModel,
    ProductType as ProductTypeModel,
    ProductUnitType as ProductUnitTypeModel,
    MasterProductPrice as MasterProductPriceModel
)
from storages.models import (
    StorageProductDetails as StorageProductDetailsModel,
)
from orders.models import (
    AgreedOrder as AgreedOrderModel,
    AgreedOrderProductDetails as AgreedOrderProductDetailsModel
)


class ProductTypeSerializer(serializers.ModelSerializer):  # OK
    class Meta:
        model = ProductTypeModel
        fields = '__all__'


class ProductUnitTypeSerializer(serializers.ModelSerializer):  # OK
    class Meta:
        model = ProductUnitTypeModel
        fields = '__all__'


class MasterProductPriceSerializer(serializers.ModelSerializer):  # OK
    class Meta:
        model = MasterProductPriceModel
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):  # OK
    product_type = ProductTypeSerializer(read_only=True)
    product_type_id = serializers.PrimaryKeyRelatedField(
        source='product_type', write_only=True,
        queryset=ProductTypeModel.objects.order_by('id').filter(removed=False))

    product_unit_type = ProductUnitTypeSerializer(read_only=True)
    product_unit_type_id = serializers.PrimaryKeyRelatedField(
        source='product_unit_type', write_only=True,
        queryset=ProductUnitTypeModel.objects.order_by('id').filter(removed=False))

    current_price = serializers.SerializerMethodField()
    available_quantity = serializers.SerializerMethodField()

    def get_current_price(self, obj):
        master_price = MasterProductPriceModel.objects.filter(
            product=obj, removed=False).order_by('created_at').reverse()
        for mprice in master_price:
            if mprice.from_date > date.today():
                continue
            if mprice.to_date >= date.today():
                return mprice.price

        return obj.base_price

    # a bit dumb but it's work for current situation
    def get_available_quantity(self, obj):
        all_input = StorageProductDetailsModel.objects.filter(
            product=obj).aggregate(all_input=Sum('amount'))['all_input'] or 0

        current_sold = AgreedOrderModel.objects.filter(
            removed=False)

        soldSum = 0
        for success_order in current_sold:
            tmp = AgreedOrderProductDetailsModel.objects.filter(
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
        model = ProductModel
        fields = '__all__'
        # exclude = ['name_latin']
