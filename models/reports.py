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
        items = session.query(Item)
        total_amount = 0
        total_cost = 0
        total_qty = 0

        for item in items:
            qty = 0
            price = 0
            for fifo_item in item.fifo_items:
                qty += fifo_item.quantity
                price = fifo_item.wholesale_price
            qty -= len(item.tran_items)
            total_qty += qty
            total_amount += qty * item.retail_price
            total_cost += float(qty) * float(price)
        
        print('Total Retail Value: {}'.format(total_amount / 100))
        print('Total Wholesale Cost: {}'.format(total_cost / 100))
        print('Total Inventory Count: {}'.format(total_qty))


if __name__ == "__main__":
    main()
