from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete, post_init

from gdstorage.storage import GoogleDriveStorage

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'admin'),
        (2, 'manager'),
        (3, 'salesman'),
        (4, 'agency'),
    )

    role = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES, default=4)


class Profile(models.Model):
    class Meta:
        db_table = 'quickstart_profile'

    # auto fields
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)

    # required
    code = models.CharField(max_length=32, unique=True, blank=True)
    address = models.CharField(max_length=256, blank=True)
    phone_number = models.CharField(max_length=16, blank=True)
    gender = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Agency(models.Model):
    class Meta:
        db_table = 'quickstart_agency'

    # auto field
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=False,
        related_name="%(class)s_created_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Tài khoản chủ sỡ hữu đại lý // Chú ý role khi gán user
    user_related = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
        related_name="%(class)s_owned_by"
    )

    code = models.CharField(max_length=32, unique=True, blank=True)
    name = models.CharField(max_length=128, blank=True)
    address = models.CharField(max_length=256, blank=True)
    phone_number = models.CharField(max_length=16, blank=True)

    # Constants priority levels
    EMERGENCY = 'EM'        # RP: < 1 hour
    URGENT = 'UR'           # RP: 24 hours
    STANDARD = 'ST'         # RP: 7 days
    NORMAL = 'NO'           # RP: Agreed date
    PRIORITY_CHOICES = (
        (EMERGENCY, 'Emergency'),
        (URGENT, 'Urgent'),
        (STANDARD, 'Standard'),
        (NORMAL, 'Normal')
    )
    priority_level = models.CharField(
        max_length=2,
        choices=PRIORITY_CHOICES,
        default=NORMAL
    )

    # permission required
    removed = models.BooleanField(default=False)
    removed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
        related_name="%(class)s_removed_by"
    )

    def __str__(self):
        return self.code


class ProductUnitType(models.Model):
    class Meta:
        db_table = 'quickstart_product_unit_type'

    # auto fields
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
        related_name="%(class)s_created_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    code = models.CharField(max_length=32, unique=True, blank=True)
    unit_type = models.CharField(max_length=128, unique=True, blank=True)

    # permission required
    removed = models.BooleanField(default=False)
    removed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
        related_name="%(class)s_removed_by"
    )

    def __str__(self):
        return self.code


class ProductType(models.Model):
    class Meta:
        db_table = 'quickstart_product_type'

    # auto fields
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
        related_name="%(class)s_created_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    code = models.CharField(max_length=32, unique=True, blank=True)
    product_type = models.CharField(max_length=128, unique=True, blank=True)

    # permission required
    removed = models.BooleanField(default=False)
    removed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
        related_name="%(class)s_removed_by"
    )


class Product(models.Model):
    class Meta:
        db_table = 'quickstart_product'

    # auto fields
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
        related_name="%(class)s_created_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, blank=True)
    product_unit_type = models.ForeignKey(
        ProductUnitType, on_delete=models.CASCADE, blank=True)

    # info
    code = models.CharField(max_length=32, unique=True, blank=True)
    name = models.CharField(max_length=256, blank=True)
    image = models.FileField(
        upload_to='images/', storage=gd_storage, blank=True)
    weight = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    base_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    origin = models.CharField(max_length=256, blank=True)

    min_reserve_quantity = models.IntegerField(default=0)

    # permission required
    removed = models.BooleanField(default=False)
    removed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
        related_name="%(class)s_removed_by"
    )

    def __str__(self):
        return self.code


class MasterProductPrice(models.Model):
    class Meta:
        db_table = 'quickstart_master_product_price'

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


class RequestOrder(models.Model):
    class Meta:
        db_table = 'quickstart_request_order'

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
        related_name="%(class)s_created_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, blank=True)
    code = models.CharField(max_length=32, unique=True, blank=True)
    bill_value = models.DecimalField(
        max_digits=11, decimal_places=2, default=0)

    # permission required
    approved = models.BooleanField(default=False)
    apprived_at = models.DateTimeField(blank=True, null=True)

    # permission required
    rejected = models.BooleanField(default=False)
    rejected_at = models.DateTimeField(blank=True, null=True)

    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.code

#     @staticmethod
#     def post_save(sender, **kwargs):
#         instance = kwargs.get('instance')
#         created = kwargs.get('created')
#         if instance.approved == True:
#             print('req order is accepted, creating agreedOrder now ...')
#             maxId = AgreedOrder.objects.all().order_by("-id").first().id
#             print('agreedOrder current max id =', maxId)
#             AgreedOrder.objects.create("AGOD" + maxId, )
#             pass


# # Signal when aproving req order
# post_save.connect(RequestOrder.post_save, sender=RequestOrder)


# This model cannot delete
class AgreedOrder(models.Model):
    class Meta:
        db_table = 'quickstart_agreed_order'

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
        related_name="%(class)s_created_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, blank=True)
    request_order = models.ForeignKey(
        RequestOrder, on_delete=models.CASCADE, blank=True)
    code = models.CharField(max_length=32, unique=True, blank=True)
    bill_value = models.DecimalField(
        max_digits=11, decimal_places=2, default=0)

    # permission required
    accepted = models.BooleanField(default=False)
    accepted_on = models.DateTimeField(blank=True, null=True)

    # permission required
    planned_for_delivery = models.BooleanField(default=False)
    expected_delivery_on = models.DateTimeField(blank=True, null=True)

    # permission required
    delivered = models.BooleanField(default=False)
    delivered_on = models.DateTimeField(blank=True, null=True)

    # PERMISSION REQUIRED
    paid = models.BooleanField(default=False)
    paid_on = models.DateTimeField(blank=True, null=True)

    removed = models.BooleanField(default=False)


class RequestOrderProductDetails(models.Model):
    class Meta:
        db_table = 'quickstart_request_order_product_details'

    # auto fields
    created_at = models.DateTimeField(auto_now_add=True)

    request_order = models.ForeignKey(
        RequestOrder, on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)


@receiver(post_save, sender=RequestOrderProductDetails)
def raise_req_bill_value(sender, instance, created, **kwargs):
    pass


class AgreedOrderProductDetails(models.Model):
    class Meta:
        db_table = 'quickstart_agreed_order_product_details'

    # auto fields
    created_at = models.DateTimeField(auto_now_add=True)

    agreed_order = models.ForeignKey(
        AgreedOrder, on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)


class Storage(models.Model):
    class Meta:
        db_table = 'quickstart_storage'

    # auto fields
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
        related_name="%(class)s_created_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    code = models.CharField(max_length=32, unique=True, blank=True)
    address = models.CharField(max_length=256, blank=True)

    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class StorageProductDetails(models.Model):
    class Meta:
        db_table = 'quickstart_storage_product_details'

    # auto fields
    created_at = models.DateTimeField(auto_now_add=True)

    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
