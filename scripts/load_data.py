import io
import csv
from django.db import connection

from products.models import (
    ProductType,
    ProductUnitType,
    Product
)
from storages.models import (
    Storage,
    StorageProductDetails
)
from users.models import (
    User,
    Profile
)
from agencies.models import (
    Agency
)


def run():
    u = User.objects.get(pk=1)
    cursor = connection.cursor()

    """
    USERS & PROFILES
    """
    fhand = io.open('scripts/users.csv', 'r',
                    encoding='utf-8-sig')
    reader = csv.reader(fhand)
    count = 0
    for index, row in enumerate(reader):
        print(index, row)
        if index == 0:
            continue
        r, created = User.objects.update_or_create(
            id=index+1,
            defaults={
                'username': row[0],
                'email': row[2],
                'first_name': row[3],
                'last_name': row[4],
                'role': row[5]
            }
        )
        r.set_password(row[1])
        r.save()
        count += 1
    cursor.execute(
        "ALTER SEQUENCE users_id_seq RESTART WITH {};".format(count+2))
    print("ALTER SEQUENCE users_id_seq RESTART WITH {};".format(count+2))

    fhand = io.open('scripts/profiles.csv', 'r',
                    encoding='utf-8-sig')
    reader = csv.reader(fhand)
    count = 0
    for index, row in enumerate(reader):
        print(index, row)
        if index == 0:
            continue
        r, created = Profile.objects.update_or_create(
            id=row[0],
            defaults={
                'user': User.objects.get(pk=row[0]),
                'gender': row[1],
                'address': row[2],
                'phone_number': row[3]
            }
        )
        count += 1
    cursor.execute(
        "ALTER SEQUENCE profiles_id_seq RESTART WITH {};".format(count+2))
    print("ALTER SEQUENCE profiles_id_seq RESTART WITH {};".format(count+2))

    """
    PRODUCTS
    """
    fhand = io.open('scripts/product_types.csv', 'r',
                    encoding='utf-8-sig')
    reader = csv.reader(fhand)
    count = 0
    for index, row in enumerate(reader):
        print(index, row)
        if index == 0:
            continue
        r, created = ProductType.objects.update_or_create(
            id=index,
            defaults={
                'code': row[0],
                'product_type': row[1],
                'created_by': u
            }
        )
        count += 1
    cursor.execute(
        "ALTER SEQUENCE product_types_id_seq RESTART WITH {};".format(count+1))
    print("ALTER SEQUENCE product_types_id_seq RESTART WITH {};".format(count+1))

    fhand = io.open('scripts/product_unit_types.csv',
                    'r', encoding='utf-8-sig')
    reader = csv.reader(fhand)
    count = 0
    for index, row in enumerate(reader):
        print(index, row)
        if index == 0:
            continue
        r, created = ProductUnitType.objects.update_or_create(
            id=index,
            defaults={
                'code': row[0],
                'unit_type': row[1],
                'created_by': u
            }
        )
        count += 1
    cursor.execute(
        "ALTER SEQUENCE product_unit_types_id_seq RESTART WITH {};".format(count+1))
    print("ALTER SEQUENCE product_unit_types_id_seq RESTART WITH {};".format(count+1))

    fhand = io.open('scripts/products.csv',
                    'r', encoding='utf-8-sig')
    reader = csv.reader(fhand)
    count = 0
    for index, row in enumerate(reader):
        print(row)
        if index == 0:
            continue
        r, created = Product.objects.update_or_create(
            id=index,
            defaults={
                'code': row[0],
                'name': row[1],
                'image': row[2],
                'weight': row[3],
                'width': row[4],
                'height': row[5],
                'base_price': row[6],
                'origin': row[7],
                'min_reserve_quantity': row[8],
                'product_type': ProductType.objects.get(pk=row[9]),
                'product_unit_type': ProductUnitType.objects.get(pk=row[10])
            }
        )
        count += 1
    cursor.execute(
        "ALTER SEQUENCE products_id_seq RESTART WITH {};".format(count+1))
    print("ALTER SEQUENCE products_id_seq RESTART WITH {};".format(count+1))

    """
    AGENCY
    """
    fhand = io.open('scripts/agencies.csv',
                    'r', encoding='utf-8-sig')
    reader = csv.reader(fhand)
    count = 0
    for index, row in enumerate(reader):
        print(row)
        if index == 0:
            continue
        user_related = User.objects.get(pk=row[5])
        r, created = Agency.objects.update_or_create(
            id=index,
            defaults={
                'code': row[0],
                'name': row[1],
                'address': row[2],
                'phone_number': row[3],
                'priority_level': row[4],
                'user_related': user_related,
                'created_by': u
            }
        )
        count += 1
    cursor.execute(
        "ALTER SEQUENCE agencies_id_seq RESTART WITH {};".format(count+1))
    print("ALTER SEQUENCE agencies_id_seq RESTART WITH {};".format(count+1))

    """
    STORAGE
    """
    fhand = io.open('scripts/storages.csv',
                    'r', encoding='utf-8-sig')
    reader = csv.reader(fhand)
    count = 0
    for index, row in enumerate(reader):
        print(row)
        if index == 0:
            continue
        r, created = Storage.objects.update_or_create(
            id=index,
            defaults={
                'code': row[0],
                'address': row[1],
                'created_by': u
            }
        )
        count += 1
    cursor.execute(
        "ALTER SEQUENCE storages_id_seq RESTART WITH {};".format(count+1))
    print("ALTER SEQUENCE storages_id_seq RESTART WITH {};".format(count+1))

    """
    STORAGE_DETAILS
    """
    fhand = io.open('scripts/storage_product_details.csv',
                    'r', encoding='utf-8-sig')
    reader = csv.reader(fhand)
    count = 0
    for index, row in enumerate(reader):
        print(row)
        if index == 0:
            continue
        r, created = StorageProductDetails.objects.get_or_create(
            id=index,
            defaults={
                'storage': Storage.objects.get(pk=row[0]),
                'product': Product.objects.get(pk=row[1]),
                'amount': row[2]
            }
        )
        count += 1
    cursor.execute(
        "ALTER SEQUENCE storage_product_details_id_seq RESTART WITH {};".format(count+1))
    print("ALTER SEQUENCE storage_product_details_id_seq RESTART WITH {};".format(count+1))
