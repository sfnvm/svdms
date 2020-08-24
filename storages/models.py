from django.db import models
from django.conf import settings

from products.models import Product

from commons.gencode import code_in_string


class Storage(models.Model):
    class Meta:
        db_table = 'storages'

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

    def save(self, *args, **kwargs):
        id = Storage.objects.count() + 1
        if not self.code:
            self.code = code_in_string(id, 'STG')
            while Storage.objects.filter(code=self.code).exists():
                id += 1
                temp = code_in_string(id, 'STG')
                self.code = code_in_string(id, 'STG')
        super(Storage, self).save()


class StorageProductDetails(models.Model):
    class Meta:
        db_table = 'storage_product_details'

    created_at = models.DateTimeField(auto_now_add=True)

    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
