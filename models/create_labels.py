#!/apps/python_3.5/bin/python3
# -*- coding: utf-8 -*-
"""Create .csv file to use to print labels."""


from datetime import datetime


# 3rd Party Imports


from sqlite_engine import session_scope
from models import Item, FIFOItem, Category, ItemCategory


__author__ = 'Brett R. Ward'

# Constants


def main():
    """Main program."""
    with session_scope() as session:
        items = session.query(Item).filter_by(manufacturer='Video Games')
        for item in items:
            qty = 0
            for fifo in item.fifo_items:
                qty += fifo.quantity
            for x in range(0, qty):
                print('{},{},{}'.format(item.sku, item.name, item.get_retail_price()))


if __name__ == "__main__":
    main()
