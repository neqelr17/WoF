#!/apps/python_3.5/bin/python3
# -*- coding: utf-8 -*-
"""Create .csv file to use to print labels."""


from datetime import datetime


# 3rd Party Imports


from sqlite_engine import session_scope
from models import Item, FIFOItem, Transaction, TransactionItem


__author__ = 'Brett R. Ward'

# Constants


def main():
    """Main program."""
    with session_scope() as session:
        item = session.query(Item).filter_by(sku='NES015').one()
        qty = 0
        print(item)
        for fifo_item in item.fifo_items:
            qty += fifo_item.quantity
            print(fifo_item)
        for tran_item in item.tran_items:
            print(tran_item)
        qty -= len(item.tran_items)
        
        print('qty: {}'.format(qty))


if __name__ == "__main__":
    main()
