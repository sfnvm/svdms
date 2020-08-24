from django.db import models
from django.conf import settings

from agencies.models import Agency as AgencyModel


class Area(models.Model):
    class Meta:
        db_table: 'area'

    code = models.CharField(max_length=32, unique=True,
                            blank=True, null=False)
    name = models.CharField(max_length=256, unique=True,
                            blank=True, null=False)
    longitude = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    latitude = models.DecimalField(max_digits=12, decimal_places=3, default=0)

    def __str__(self):
        return self.name


class SalesmanAreaDetails(models.Model):
    class Meta:
        db_table: 'salesman_area_details'

    area = models.OneToOneField(
        Area, on_delete=models.CASCADE, blank=True
    )
    salesman = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True
    )


class AgencyAreaDetails(models.Model):
    class Meta:
        db_table: 'agency_area_details'

    area = models.OneToOneField(
        Area, on_delete=models.CASCADE, blank=True
    )
    agency = models.OneToOneField(
        AgencyModel, on_delete=models.CASCADE, blank=True
    )
