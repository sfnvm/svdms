# Generated by Django 3.0.7 on 2020-08-26 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20200825_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agreedorder',
            name='status',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'wait_agency'), (10, 'agency_rejected'), (11, 'agency_approved'), (20, 'rejected'), (21, 'approved'), (33, 'planned_for_delivery'), (44, 'delivered')], default=0),
        ),
    ]
