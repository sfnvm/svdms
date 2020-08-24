from django.db import models
from django.conf import settings


class Area(models.Model):
    class Meta:
        db_table: 'area'

    # code ?
    code = models.CharField(max_length=32, unique=True,
                            blank=True, null=False)
    name = models.CharField(max_length=256, unique=True,
                            blank=True, null=False)

    def __str__(self):
        return self.name


class SalesmanAreaDetails(models.Model):
    class Meta:
        db_table: 'salesman_area_details'

    area = models.OneToOneField(
        Area, on_delete=models.CASCADE, blank=True
    )
