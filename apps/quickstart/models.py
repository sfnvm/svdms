from django.db import models
from django.conf import settings
from django.utils import timezone


class Agency(models.Model):
    class Meta:
        db_table = 'quickstart_agency'
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True
    )
    code = models.CharField(max_length=32, blank=True)
    name = models.CharField(max_length=128, blank=True)
    address = models.CharField(max_length=256, default='update is required')
    phone_number = models.CharField(max_length=16, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.code


class ProductUnitType(models.Model):
    class Meta:
        db_table = 'quickstart_product_unit_type'

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
    )
    code = models.CharField(max_length=32, unique=True, blank=True)
    unit_type = models.CharField(max_length=128, unique=True, blank=True)


class ProductType(models.Model):
    class Meta:
        db_table = 'quickstart_product_type'

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
    )
    code = models.CharField(max_length=32, unique=True, blank=True)
    name = models.CharField(max_length=128, unique=True, blank=True)


class MasterProductPrice(models.Model):
    class Meta:
        db_table = 'quickstart_master_product_price'

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
    )
    code = models.CharField(max_length=32, unique=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    from_date = models.DateField(blank=True)
    to_date = models.DateField(blank=True)


class Product(models.Model):
    class Meta:
        db_table = 'quickstart_product'

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
    )
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, blank=True)
    product_unit_type = models.ForeignKey(
        ProductUnitType, on_delete=models.CASCADE, blank=True)
    code = models.CharField(max_length=32, unique=True, blank=True)
    name = models.CharField(max_length=256, blank=True)
    image_url = models.CharField(max_length=1024, blank=True)
    weight = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    # price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    origin = models.CharField(max_length=256, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class Order(models.Model):
    class Meta:
        db_table = 'quickstart_order'

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
    )
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, blank=True)
    code = models.CharField(max_length=32, unique=True, blank=True)
    bill_value = models.DecimalField(
        max_digits=11, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class OrderProductDetails(models.Model):
    class Meta:
        db_table = 'quickstart_order_product_details'

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)


class Storage(models.Model):
    class Meta:
        db_table = 'quickstart_storage'

    code = models.CharField(max_length=32, unique=True, blank=True)
    address = models.CharField(max_length=256, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.code


class StorageProductDetails(models.Model):
    class Meta:
        db_table = 'quickstart_storage_product_details'

    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)