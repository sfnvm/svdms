# Generated by Django 3.0.7 on 2020-08-25 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agencies', '0002_auto_20200824_1215'),
        ('areas', '0005_area_name_latin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areaagencydetails',
            name='agency',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='agencies.Agency'),
        ),
        migrations.AlterField(
            model_name='areaagencydetails',
            name='area',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='areas.Area'),
        ),
        migrations.AlterField(
            model_name='areasalesmandetails',
            name='area',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='areas.Area'),
        ),
        migrations.AlterField(
            model_name='areasalesmandetails',
            name='salesman',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]