from django.db import models
from django.conf import settings

from django.dispatch import receiver
from django.db.models.signals import pre_save

from gdstorage.storage import GoogleDriveStorage

from commons.convert_vietnamese import no_accent_vietnamese

gd_storage = GoogleDriveStorage()


class ProductUnitType(models.Model):
    class Meta:
        db_table = 'product_unit_types'

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
        related_name="%(class)s_created_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    code = models.CharField(max_length=32, unique=True, blank=True)
    unit_type = models.CharField(max_length=128, unique=True, blank=True)

    removed = models.BooleanField(default=False)
    removed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
        related_name="%(class)s_removed_by"
    )

    def __str__(self):
        return self.code


class ProductType(models.Model):
    class Meta:
        db_table = 'product_types'

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
        related_name="%(class)s_created_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    code = models.CharField(max_length=32, unique=True, blank=True)
    product_type = models.CharField(max_length=128, unique=True, blank=True)

    removed = models.BooleanField(default=False)
    removed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
        related_name="%(class)s_removed_by"
    )


class Product(models.Model):
    class Meta:
        db_table = 'products'

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
        related_name="%(class)s_created_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, blank=True)
    product_unit_type = models.ForeignKey(
        ProductUnitType, on_delete=models.CASCADE, blank=True)

    code = models.CharField(max_length=32, unique=True, blank=True)
    name = models.CharField(max_length=256, blank=True)
    name_latin = models.CharField(max_length=256, blank=True,)
    image = models.FileField(
        upload_to='images/', storage=gd_storage, blank=True)
    weight = models.DecimalField(max_digits=9, decimal_places=5, default=0)
    width = models.DecimalField(max_digits=9, decimal_places=5, default=0)
    height = models.DecimalField(max_digits=9, decimal_places=5, default=0)
    base_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    origin = models.CharField(max_length=256, blank=True)

    min_reserve_quantity = models.IntegerField(default=0)

    removed = models.BooleanField(default=False)
    removed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
        related_name="%(class)s_removed_by"
    )

    def __str__(self):
        return self.code


def pre_save_product(sender, instance, **kwargs):
    instance.name_latin = no_accent_vietnamese(instance.name)


pre_save.connect(pre_save_product, sender=Product)


class MasterProductPrice(models.Model):
    class Meta:
        db_table = 'master_product_prices'

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
        related_name="%(class)s_created_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    code = models.CharField(max_length=32, unique=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    from_date = models.DateField(blank=True)
    to_date = models.DateField(blank=True)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.code
