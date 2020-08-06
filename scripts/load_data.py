import io
import csv

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


def run():
    u = User.objects.get(pk=1)

    """
    USERS & PROFILES
    """
    fhand = io.open('scripts/users.csv', 'r',
                    encoding='utf-8-sig')
    reader = csv.reader(fhand)
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

    fhand = io.open('scripts/profiles.csv', 'r',
                    encoding='utf-8-sig')
    reader = csv.reader(fhand)
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

    """
    PRODUCTS
    """
    fhand = io.open('scripts/product_types.csv', 'r',
                    encoding='utf-8-sig')
    reader = csv.reader(fhand)
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

    fhand = io.open('scripts/product_unit_types.csv',
                    'r', encoding='utf-8-sig')
    reader = csv.reader(fhand)
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

    fhand = io.open('scripts/products.csv',
                    'r', encoding='utf-8-sig')
    reader = csv.reader(fhand)
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

    """
    STORAGE
    """
    fhand = io.open('scripts/storages.csv',
                    'r', encoding='utf-8-sig')
    reader = csv.reader(fhand)
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

    fhand = io.open('scripts/storage_product_details.csv',
                    'r', encoding='utf-8-sig')
    reader = csv.reader(fhand)
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
