from django.db import models
from django.conf import settings

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete, post_delete, post_init

from agencies.models import Agency as AgencyModel
from products.models import Product as ProductModel

from commons.utils import get_current_product_price
from commons.gencode import code_in_string


class RequestOrder(models.Model):
    class Meta:
        db_table = 'request_orders'

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
        related_name="%(class)s_created_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    agency = models.ForeignKey(
        AgencyModel, on_delete=models.CASCADE, blank=True)
    code = models.CharField(max_length=32, unique=True, blank=True)
    bill_value = models.DecimalField(
        max_digits=20, decimal_places=2, default=0)

    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(blank=True, null=True)

    rejected = models.BooleanField(default=False)
    rejected_at = models.DateTimeField(blank=True, null=True)

    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        id = RequestOrder.objects.count() + 1
        if not self.code:
            self.code = code_in_string(id, 'RQO')
            while RequestOrder.objects.filter(code=self.code).exists():
                id += 1
                temp = code_in_string(id, 'RQO')
                self.code = code_in_string(id, 'RQO')
        super(RequestOrder, self).save()


class AgreedOrder(models.Model):
    class Meta:
        db_table = 'agreed_orders'

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
        related_name="%(class)s_created_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    agency = models.ForeignKey(
        AgencyModel, on_delete=models.CASCADE, blank=True)
    request_order = models.OneToOneField(
        RequestOrder, on_delete=models.CASCADE, blank=True)
    code = models.CharField(max_length=32, unique=True, blank=True, null=False)
    bill_value = models.DecimalField(
        max_digits=20, decimal_places=2, default=0)

    STATUS = (
        (00, 'wait_agency'),
        (10, 'agency_rejected'),
        (11, 'agency_approved'),
        (20, 'rejected'),
        (21, 'approved'),
        (33, 'planned_for_delivery'),
        (44, 'delivered')
    )
    status = models.PositiveSmallIntegerField(
        choices=STATUS, blank=True, default=00, null=False)

    approved = models.BooleanField(default=False)
    approved_on = models.DateTimeField(blank=True, null=True)

    rejected = models.BooleanField(default=False)
    rejected_on = models.DateTimeField(blank=True, null=True)

    agency_rejected = models.BooleanField(default=False)
    agency_rejected_on = models.DateTimeField(blank=True, null=True)

    agency_accepted = models.BooleanField(default=False)
    agency_accepted_on = models.DateTimeField(blank=True, null=True)

    planned_for_delivery = models.BooleanField(default=False)
    expected_delivery_on = models.DateTimeField(blank=True, null=True)

    delivered = models.BooleanField(default=False)
    delivered_on = models.DateTimeField(blank=True, null=True)

    paid = models.BooleanField(default=False)
    paid_on = models.DateTimeField(blank=True, null=True)
    confirm_paid_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
        related_name="%(class)s_confirm_paid_by"
    )

    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        id = AgreedOrder.objects.count() + 1
        if not self.code:
            self.code = code_in_string(id, 'AGO')
            while AgreedOrder.objects.filter(code=self.code).exists():
                id += 1
                temp = code_in_string(id, 'AGO')
                self.code = code_in_string(id, 'AGO')
        super(AgreedOrder, self).save()


class RequestOrderProductDetails(models.Model):
    class Meta:
        db_table = 'request_order_product_details'

    created_at = models.DateTimeField(auto_now_add=True)

    request_order = models.ForeignKey(
        RequestOrder, on_delete=models.CASCADE
    )
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    negotiated_price = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    amount = models.IntegerField(default=0)


def increase_req_bill_value(sender, instance, created, **kwargs):
    if created:
        current_price = get_current_product_price(
            instance.product.id)
        in_total = current_price * int(instance.amount)
        instance.request_order.bill_value = instance.request_order.bill_value + in_total
        instance.request_order.save()


def decreate_req_bill_value(sender, instance, **kwargs):
    in_total = instance.negotiated_price * instance.amount
    instance.request_order.bill_value = instance.request_order.bill_value - in_total
    instance.request_order.save()


post_save.connect(increase_req_bill_value, sender=RequestOrderProductDetails)
pre_delete.connect(decreate_req_bill_value, sender=RequestOrderProductDetails)


class AgreedOrderProductDetails(models.Model):
    class Meta:
        db_table = 'agreed_order_product_details'

    created_at = models.DateTimeField(auto_now_add=True)

    agreed_order = models.ForeignKey(
        AgreedOrder, on_delete=models.CASCADE
    )
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    request_amount = models.IntegerField(default=0)
    negotiated_price = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)


def increase_agr_bill_value(sender, instance, created, **kwargs):
    if created:
        current_price = get_current_product_price(
            instance.product.id)
        in_total = current_price * instance.amount
        instance.agreed_order.bill_value = instance.agreed_order.bill_value + in_total
        instance.agreed_order.save()


def decreate_agr_bill_value(sender, instance, **kwargs):
    in_total = instance.negotiated_price * instance.amount
    instance.agreed_order.bill_value = instance.agreed_order.bill_value - in_total
    instance.agreed_order.save()


post_save.connect(increase_agr_bill_value, sender=AgreedOrderProductDetails)
pre_delete.connect(decreate_agr_bill_value, sender=AgreedOrderProductDetails)
