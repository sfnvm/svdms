# Generated by Django 3.0.7 on 2020-08-24 12:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('areas', '0001_initial'),
        ('agencies', '0002_auto_20200824_1215'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='salesmanareadetails',
            name='salesman',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='agencyareadetails',
            name='agency',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='agencies.Agency'),
        ),
        migrations.AddField(
            model_name='agencyareadetails',
            name='area',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='areas.Area'),
        ),
    ]
