from django.db import models
from django.conf import settings

from agencies.models import Agency as AgencyModel

from commons.gencode import code_in_string
from commons.convert_vietnamese import no_accent_vietnamese


class Area(models.Model):
    class Meta:
        db_table: 'areas'

    code = models.CharField(max_length=32, unique=True,
                            blank=True, null=False)
    name = models.CharField(max_length=256, unique=True,
                            blank=True, null=False)
    name_latin = models.CharField(max_length=256,
                                  blank=True, null=False)
    longitude = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    latitude = models.DecimalField(max_digits=12, decimal_places=3, default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        id = Area.objects.count() + 1
        if not self.code:
            self.code = code_in_string(id, 'ARA')
            while Area.objects.filter(code=self.code).exists():
                id += 1
                temp = code_in_string(id, 'ARA')
                self.code = code_in_string(id, 'ARA')
        if self.name:
            self.name_latin = no_accent_vietnamese(self.name)
        super(Area, self).save()


class AreaSalesmanDetails(models.Model):
    class Meta:
        db_table: 'salesman_area_details'
        unique_together = ('area', 'salesman')

    area = models.ForeignKey(
        Area, on_delete=models.CASCADE, blank=True
    )
    salesman = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True
    )


class AreaAgencyDetails(models.Model):
    class Meta:
        db_table: 'agency_area_details'
        unique_together = ('area', 'agency')

    area = models.ForeignKey(
        Area, on_delete=models.CASCADE, blank=True
    )
    agency = models.ForeignKey(
        AgencyModel, on_delete=models.CASCADE, blank=True
    )
