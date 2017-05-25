#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""WoF inventory and POS models.


"""

import datetime


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, ForeignKey, Sequence, UniqueConstraint
from sqlalchemy.types import Boolean, DateTime, Integer, SmallInteger, String


__author__ = 'Brett R. Ward'


# Constants
ENCODING = 'utf-8'

# Create base for model objects to inherit.
BASE = declarative_base()


class Item(BASE):
    """Inventory item.

    Describes an item in inventory.
    """

    __tablename__ = 'items'

    # Columns
    id = Column(Integer, Sequence('user_id'), primary_key=True)
    sku = Column(String(8), nullable=False, unique=True)
    upc = Column(Integer, nullable=True)
    name = Column(String(50), nullable=False)
    retail_price = Column(Integer(), nullable=False)

    # Relationships

    def __init__(self, *args, **kwargs):
        """Init magic method."""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """Print User pretty when cast as a string."""
        return 'Item(id={}, sku={}, name={}, retail price={}, upc={})'.format(
            self.id,
            self.sku,
            self.name,
            self.retail_price,
            self.upc)

    def __repr__(self):
        """Print User pretty when called in python repl."""
        return '<{}>'.format(self.__str__())


class FIFOItem(BASE):
    """Item meta that contains cost of quantities purchased.

    Will be consumed using FIFO.
    """

    __tablename__ = 'fifo_items'

    # Columns
    id = Column(Integer, Sequence('user_id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    wholesale_price = Column(Integer(), nullable=False)
    quantity = Column(Integer, nullable=False)
    acqusition_date = Column(DateTime, nullable=False)

    # Relationships
    item = relationship('Item', foreign_keys=item_id, backref='fifo_items')

    def __init__(self, *args, **kwargs):
        """Init magic method."""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """Print User pretty when cast as a string."""
        return 'FIFOItem(id={}, item={}, price={}, quantity={}, date={})'.format(
            self.id,
            self.item.name,
            self.wholesale_price,
            self.quantity,
            self.acqusition_date)

    def __repr__(self):
        """Print User pretty when called in python repl."""
        return '<{}>'.format(self.__str__())
