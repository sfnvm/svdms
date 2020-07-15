from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=32, unique=True, blank=True)
    address = models.CharField(max_length=256, blank=True)
    phone_number = models.CharField(max_length=16, blank=True)
    gender = models.BooleanField(default=True)

    def __str__(self):
        return self.code


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


# @receiver(pre_delete, sender=User)
# def delete_profile_for_user(sender, instance=None, **kwargs):
#     if instance:
#         user_profile = Profile.objects.get(user=instance)
#         user_profile.delete()


class Agency(models.Model):
    class Meta:
        db_table = 'quickstart_agency'

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    code = models.CharField(max_length=32, blank=True)
    name = models.CharField(max_length=128, blank=True)
    address = models.CharField(max_length=256, blank=True)
    phone_number = models.CharField(max_length=16, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    removed = models.BooleanField(default=False)

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
    created_at = models.DateTimeField(auto_now_add=True)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class ProductType(models.Model):
    class Meta:
        db_table = 'quickstart_product_type'

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
    )
    code = models.CharField(max_length=32, unique=True, blank=True)
    product_type = models.CharField(max_length=128, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    removed = models.BooleanField(default=False)


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
    base_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    origin = models.CharField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class MasterProductPrice(models.Model):
    class Meta:
        db_table = 'quickstart_master_product_price'

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    code = models.CharField(max_length=32, unique=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    from_date = models.DateField(blank=True)
    to_date = models.DateField(blank=True)

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
    created_at = models.DateTimeField(auto_now_add=True)
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
    created_at = models.DateTimeField(auto_now_add=True)


class Storage(models.Model):
    class Meta:
        db_table = 'quickstart_storage'

    code = models.CharField(max_length=32, unique=True, blank=True)
    address = models.CharField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


class StorageProductDetails(models.Model):
    class Meta:
        db_table = 'quickstart_storage_product_details'

    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
