# Generated by Django 3.0.7 on 2020-08-23 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20200823_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productunittype',
            name='code',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
