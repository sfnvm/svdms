# Generated by Django 3.0.7 on 2020-08-25 14:40

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agencies', '0002_auto_20200824_1215'),
        ('areas', '0002_auto_20200824_1215'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AgencyAreaDetails',
            new_name='AreaAgencyDetails',
        ),
        migrations.RenameModel(
            old_name='SalesmanAreaDetails',
            new_name='AreaSalesmanDetails',
        ),
    ]
