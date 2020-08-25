# Generated by Django 3.0.7 on 2020-08-24 12:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agencies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='created_by',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='agency_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='agency',
            name='removed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agency_removed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='agency',
            name='user_related',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agency_owned_by', to=settings.AUTH_USER_MODEL),
        ),
    ]