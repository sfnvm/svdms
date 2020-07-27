# Generated by Django 3.0.7 on 2020-07-27 08:35

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.PositiveSmallIntegerField(choices=[(1, 'admin'), (2, 'manager'), (3, 'salesman'), (4, 'agency')], default=4)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(blank=True, max_length=32, unique=True)),
                ('name', models.CharField(blank=True, max_length=128)),
                ('address', models.CharField(blank=True, max_length=256)),
                ('phone_number', models.CharField(blank=True, max_length=16)),
                ('priority_level', models.CharField(choices=[('EM', 'Emergency'), ('UR', 'Urgent'), ('ST', 'Standard'), ('NO', 'Normal')], default='NO', max_length=2)),
                ('removed', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='agency_created_by', to=settings.AUTH_USER_MODEL)),
                ('removed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agency_removed_by', to=settings.AUTH_USER_MODEL)),
                ('user_related', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agency_owned_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'quickstart_agency',
            },
        ),
        migrations.CreateModel(
            name='AgreedOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(blank=True, max_length=32, unique=True)),
                ('bill_value', models.DecimalField(decimal_places=2, default=0, max_digits=11)),
                ('accepted', models.BooleanField(default=False)),
                ('accepted_on', models.DateTimeField(blank=True, null=True)),
                ('planned_for_delivery', models.BooleanField(default=False)),
                ('expected_delivery_on', models.DateTimeField(blank=True, null=True)),
                ('delivered', models.BooleanField(default=False)),
                ('delivered_on', models.DateTimeField(blank=True, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('paid_on', models.DateTimeField(blank=True, null=True)),
                ('removed', models.BooleanField(default=False)),
                ('agency', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='quickstart.Agency')),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='agreedorder_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'quickstart_agreed_order',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(blank=True, max_length=32, unique=True)),
                ('name', models.CharField(blank=True, max_length=256)),
                ('image_url', models.CharField(blank=True, max_length=1024)),
                ('weight', models.IntegerField(default=0)),
                ('width', models.IntegerField(default=0)),
                ('height', models.IntegerField(default=0)),
                ('base_price', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('origin', models.CharField(blank=True, max_length=256)),
                ('min_reserve_quantity', models.IntegerField(default=0)),
                ('removed', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'quickstart_product',
            },
        ),
        migrations.CreateModel(
            name='RequestOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(blank=True, max_length=32, unique=True)),
                ('bill_value', models.DecimalField(decimal_places=2, default=0, max_digits=11)),
                ('approved', models.BooleanField(default=False)),
                ('apprived_at', models.DateTimeField(blank=True, null=True)),
                ('rejected', models.BooleanField(default=False)),
                ('rejected_at', models.DateTimeField(blank=True, null=True)),
                ('removed', models.BooleanField(default=False)),
                ('agency', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='quickstart.Agency')),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='requestorder_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'quickstart_request_order',
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(blank=True, max_length=32, unique=True)),
                ('address', models.CharField(blank=True, max_length=256)),
                ('removed', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='storage_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'quickstart_storage',
            },
        ),
        migrations.CreateModel(
            name='StorageProductDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('amount', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.Product')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.Storage')),
            ],
            options={
                'db_table': 'quickstart_storage_product_details',
            },
        ),
        migrations.CreateModel(
            name='RequestOrderProductDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('amount', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.Product')),
                ('request_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.RequestOrder')),
            ],
            options={
                'db_table': 'quickstart_request_order_product_details',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=32, unique=True)),
                ('address', models.CharField(blank=True, max_length=256)),
                ('phone_number', models.CharField(blank=True, max_length=16)),
                ('gender', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'quickstart_profile',
            },
        ),
        migrations.CreateModel(
            name='ProductUnitType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(blank=True, max_length=32, unique=True)),
                ('unit_type', models.CharField(blank=True, max_length=128, unique=True)),
                ('removed', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='productunittype_created_by', to=settings.AUTH_USER_MODEL)),
                ('removed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productunittype_removed_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'quickstart_product_unit_type',
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(blank=True, max_length=32, unique=True)),
                ('product_type', models.CharField(blank=True, max_length=128, unique=True)),
                ('removed', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='producttype_created_by', to=settings.AUTH_USER_MODEL)),
                ('removed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='producttype_removed_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'quickstart_product_type',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='quickstart.ProductType'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_unit_type',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='quickstart.ProductUnitType'),
        ),
        migrations.AddField(
            model_name='product',
            name='removed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_removed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='MasterProductPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(blank=True, max_length=32, unique=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('from_date', models.DateField(blank=True)),
                ('to_date', models.DateField(blank=True)),
                ('removed', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='masterproductprice_created_by', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='quickstart.Product')),
            ],
            options={
                'db_table': 'quickstart_master_product_price',
            },
        ),
        migrations.CreateModel(
            name='AgreedOrderProductDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('amount', models.IntegerField(default=0)),
                ('agreed_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.AgreedOrder')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.Product')),
            ],
            options={
                'db_table': 'quickstart_agreed_order_product_details',
            },
        ),
        migrations.AddField(
            model_name='agreedorder',
            name='request_order',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='quickstart.RequestOrder'),
        ),
    ]
