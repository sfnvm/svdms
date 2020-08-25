from datetime import date, datetime

from django.db.models import Sum

from products.models import (
    Product,
    MasterProductPrice
)
from storages.models import (
    StorageProductDetails
)
import orders.models


def get_current_product_price(product_id):
    obj = Product.objects.filter(id=product_id).first()
    master_price = MasterProductPrice.objects.filter(
        product=obj, removed=False).order_by('created_at').reverse()
    for mprice in master_price:
        if mprice.from_date > date.today():
            continue
        if mprice.to_date >= date.today():
            return mprice.price
    return obj.base_price


def get_product_price_by_date(product_id, timestamp):
    obj = Product.objects.filter(id=product_id).first()
    master_price = MasterProductPrice.objects.filter(
        product=obj, removed=False).order_by('created_at').reverse()
    for mprice in master_price:
        if mprice.from_date > timestamp.date():
            continue
        if mprice.to_date >= timestamp.date():
            return mprice.price
    return obj.base_price


def get_available_product_quantity(product_id):
    obj = Product.objects.filter(id=product_id).first()
    all_input = StorageProductDetails.objects.filter(
        product=obj).aggregate(all_input=Sum('amount'))['all_input'] or 0

    # delivered=True, paid=True
    current_sold = orders.models.AgreedOrder.objects.filter(removed=False)

    soldSum = 0
    for success_order in current_sold:
        tmp = orders.models.AgreedOrderProductDetails.objects.filter(
            agreed_order=success_order, product=obj).aggregate(tmp=Sum('amount'))['tmp'] or 0
        if tmp:
            soldSum += tmp

    return all_input - soldSum
