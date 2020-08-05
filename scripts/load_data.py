import io
import csv

from products.models import (
    ProductType,
    ProductUnitType,
    Product
)
from users.models import (
    User
)


def run():
    u = User.objects.get(pk=1)

    fhand = io.open('scripts/product_types.csv', 'r',
                    encoding='utf-8-sig')
    reader = csv.reader(fhand)
    for index, row in enumerate(reader):
        print(index, row)
        if index == 0:
            continue
        r, created = ProductType.objects.get_or_create(
            id=index,
            code=row[0],
            product_type=row[1],
            created_by=u
        )

    fhand = io.open('scripts/product_unit_types.csv',
                    'r', encoding='utf-8-sig')
    reader = csv.reader(fhand)
    for index, row in enumerate(reader):
        print(index, row)
        if index == 0:
            continue
        r, created = ProductUnitType.objects.get_or_create(
            id=index,
            code=row[0],
            unit_type=row[1],
            created_by=u
        )

    fhand = io.open('scripts/products.csv',
                    'r', encoding='utf-8-sig')
    reader = csv.reader(fhand)
    for index, row in enumerate(reader):
        print(row)
        if index == 0:
            continue
        r, created = Product.objects.get_or_create(
            id=row[0],
            code=row[1],
            name=row[2],
            image=row[3],
            weight=row[4],
            width=row[5],
            height=row[6],
            base_price=row[7],
            origin=row[8],
            min_reserve_quantity=row[9],
            product_type=ProductType.objects.get(pk=row[10]),
            product_unit_type=ProductUnitType.objects.get(pk=row[11])
        )
