from django.db import models
from django.conf import settings


class Area(models.Model):
    class Meta:
        db_table: 'area'

    # code ?
    name = models.CharField(max_length=256, blank=True, null=False)
