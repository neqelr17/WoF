#!/apps/python_3.5/bin/python3
# -*- coding: utf-8 -*-
"""Import inventory from xlsx file.

Uses openpyxl.
"""

from datetime import datetime
from enum import Enum


import openpyxl


from sqlite_engine import session_scope
from models import Item, FIFOItem, Category, ItemCategory


__author__ = 'Brett R. Ward'

# Constants


class Header(Enum):
    """Enum to remember header positions."""

    sku = 0
    name = 1
    category = 2
    wholesale_price = 3
    retail_price = 4
    quantity = 5
    barcode = 6


def main():
    """Main program."""
    with session_scope() as session:
        workbook = openpyxl.load_workbook('WoF_inventory.xlsx')
        print(workbook.get_sheet_names())
        for manufacturer in workbook.get_sheet_names():
            sheet = workbook.get_sheet_by_name(manufacturer)
            for row in sheet.iter_rows():
                if row[Header.sku.value].value != 'SKU':
                    item = get_create_item(session, row, manufacturer)
                    category = get_create_category(
                        session, row[Header.category.value].value)
                    set_item_category(session, item, category)
                    create_fifo_item(session, item, row)


def create_fifo_item(session, item, row):
    """Create a new fifo item entry."""
    if row[Header.quantity.value].value is not None:
        fifo_item = FIFOItem(item=item, acqusition_date=datetime.utcnow())
        fifo_item.set_quantity(row[Header.quantity.value].value)
        fifo_item.set_wholesale_price(row[Header.wholesale_price.value].value)


def set_item_category(session, item, category):
    """Check for item cat relationship if not exist create one."""
    item_cat = session.query(ItemCategory).filter_by(
        item=item, category=category).first()
    if item_cat is None:
        item_cat = ItemCategory(item=item, category=category)
        session.add(item_cat)


def get_create_item(session, row, manufacturer):
    """Query for item, if does not exist create one."""
    item = session.query(Item).filter_by(
        sku=row[Header.sku.value].value).first()
    if item is None:
        item = Item(sku=row[Header.sku.value].value,
                    name=row[Header.name.value].value,
                    manufacturer=manufacturer)
        item.set_retail_price(row[Header.retail_price.value].value)
        session.add(item)
    return item


def get_create_category(session, cat_name):
    """Query for category, if does not exist create one."""
    cat = session.query(Category).filter_by(name=cat_name).first()
    if cat is None:
        cat = Category(name=cat_name)
        session.add(cat)
    return cat


if __name__ == "__main__":
    main()
