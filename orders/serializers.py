from django.utils import timezone

from rest_framework import serializers

from products.models import Product as ProductModel
from agencies.models import Agency as AgencyModel
from orders.models import (
    AgreedOrder as AgreedOrderModel,
    RequestOrder as RequestOrderModel,
    RequestOrderProductDetails as RequestOrderProductDetailsModel,
    AgreedOrderProductDetails as AgreedOrderProductDetailsModel
)

from products.serializers import ProductSerializer
from agencies.serializers import AgencySerializer

from commons.utils import (
    get_available_product_quantity,
    get_current_product_price
)

from commons import mails_worker


class RequestOrderProductDetailsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        source='product', write_only=True,
        queryset=ProductModel.objects.order_by('id').filter(removed=False))

    class Meta:
        model = RequestOrderProductDetailsModel
        exclude = ['request_order']

    def validate(self, data):
        if int(data['amount']) > get_available_product_quantity(data['product_id']):
            raise serializers.ValidationError(
                {"amount_error": "Cannot satisfy product quantity. REASON: NOT ENOUGH PRODUCT IN STORAGE",
                 "details": f"{data['product_id']}"})
        return data


class AgreedOrderProductDetailsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        source='product', write_only=True,
        queryset=ProductModel.objects.order_by('id').filter(removed=False))

    class Meta:
        model = AgreedOrderProductDetailsModel
        fields = '__all__'


class RequestOrderSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True)

    agency = AgencySerializer(read_only=True)
    agency_id = serializers.PrimaryKeyRelatedField(
        source='agency', write_only=True,
        queryset=AgencyModel.objects.order_by('id').filter(removed=False))

    # source='requestorderproductdetails_set'
    requestorderproductdetails_set = RequestOrderProductDetailsSerializer(
        many=True, read_only=True)
    details = serializers.JSONField(write_only=True)

    class Meta:
        model = RequestOrderModel
        fields = '__all__'
        read_only_fields = ['bill_value']

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related(
            'requestorderproductdetails_set',
            'requestorderproductdetails_set__product'
        )
        return queryset

    def approving(self, user, data):
        data.approved = True
        data.approved_at = timezone.now()
        data.save()
        instance = {
            'created_by': user,
            'request_order': data,
            'details': []
        }
        result = AgreedOrderSerializer.create(AgreedOrderSerializer, instance)

        mails_worker.request_order_confirmed(
            data.agency.user_related.email,
            result.code,
            user.username,
            user.profile.phone_number
        )

        return data

    def rejecting(self):
        pass

    def create(self, validated_data):
        request_order_data = validated_data.pop('details')

        # Validated amount
        for req_order in request_order_data:
            RequestOrderProductDetailsSerializer.validate(
                RequestOrderProductDetailsSerializer,
                req_order)

        request_order = RequestOrderModel.objects.create(
            **validated_data)

        for req_order in request_order_data:
            RequestOrderProductDetailsModel.objects.create(
                request_order=request_order,
                negotiated_price=get_current_product_price(
                    req_order['product_id']),
                **req_order)

        if request_order.approved:
            self.approving(validated_data['created_by'], request_order)

        return request_order

    def update(self, instance, validated_data):
        request_order_data = validated_data.pop('details')

        # Validated ammout
        for req_order in request_order_data:
            RequestOrderProductDetailsSerializer.validate(
                RequestOrderProductDetailsSerializer,
                req_order)

        instance.__dict__.update(**validated_data)
        instance.save()

        RequestOrderProductDetailsModel.objects.filter(
            request_order=instance).delete()

        instance = RequestOrderModel.objects.filter(
            id=instance.id).first()

        # TODO 500
        for req_order in request_order_data:
            RequestOrderProductDetailsModel.objects.create(
                request_order=instance,
                negotiated_price=get_current_product_price(
                    req_order['product_id']),
                **req_order)

        result = RequestOrderModel.objects.filter(id=instance.id).first()

        if result.approved:
            self.approving(validated_data['created_by'], result)

        return result


class AgreedOrderSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True)

    agency = AgencySerializer(read_only=True)
    # agency_id = serializers.PrimaryKeyRelatedField(
    #     source='agency', write_only=True,
    #     queryset=AgencyModel.objects.order_by('id').filter(removed=False))

    # request_order = RequestOrderSerializer(read_only=True)
    # request_order_id = serializers.PrimaryKeyRelatedField(
    #     source='request_order', write_only=True,
    #     queryset=RequestOrderModel.objects.order_by(
    #         'id').filter(removed=False))

    agreedorderproductdetails_set = AgreedOrderProductDetailsSerializer(
        many=True, read_only=True)
    # details = serializers.JSONField(
    #     write_only=True)

    class Meta:
        model = AgreedOrderModel
        fields = '__all__'
        read_only_fields = ['bill_value']

    def create(self, validated_data):
        agreed_order_data = validated_data.pop('details')
        agreed_order = AgreedOrderModel.objects.create(agency=validated_data['request_order'].agency,
                                                       ** validated_data)

        # get all req order current in new stage
        unprocessed_request_orders = RequestOrderModel.objects.order_by(
            'id').filter(removed=False, rejected=False, approved=False)

        # cal product amount can provide
        products_current_req = {}
        for unprocessed_request_order in unprocessed_request_orders:
            details = RequestOrderProductDetailsModel.objects.filter(
                request_order=unprocessed_request_order)
            for req_detail in details:
                if req_detail.product.id not in products_current_req:
                    products_current_req[req_detail.product.id] = req_detail.amount
                else:
                    products_current_req[req_detail.product.id] += req_detail.amount

        request_order_details = RequestOrderProductDetailsModel.objects.filter(
            request_order=validated_data['request_order'])

        for detail in request_order_details:
            amount_can_provide = 0
            if get_available_product_quantity(
                    detail.product.id) > detail.amount + int(products_current_req.get(detail.product.id) or 0):
                amount_can_provide = detail.amount
            else:
                amount_can_provide = int(get_available_product_quantity(
                    detail.product.id) * (detail.amount/(detail.amount + int(products_current_req.get(detail.product.id) or 0))))

            AgreedOrderProductDetailsModel.objects.create(
                product=detail.product,
                negotiated_price=detail.negotiated_price,
                agreed_order=agreed_order,
                request_amount=detail.amount,
                amount=amount_can_provide)

        return agreed_order

    # def update(self, instance, validated_data):
    #     pass
