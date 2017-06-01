#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""WoF inventory and POS models.

Contains SQLAlchemy models. These can be used in python as objects or to create
the database with all of its constraints.
"""

# STD Library imports


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, ForeignKey, Sequence, UniqueConstraint
from sqlalchemy.types import DateTime, DECIMAL, Integer, String


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
    manufacturer = Column(String(50), nullable=True)

    # Relationships
    # categories via backref
    # fifo_items via backref

    def __init__(self, *args, **kwargs):
        """Init magic method."""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """Print User when cast as a string."""
        return 'Item(id={}, sku={}, name={}, retail price={}, upc={})'.format(
            self.id,
            self.sku,
            self.name,
            self.retail_price,
            self.upc)

    def __repr__(self):
        """Print User when called in python repl."""
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
        """Print User when cast as a string."""
        return ('FIFOItem(id={}, item={}, price={},'
                ' quantity={}, date={})').format(
                    self.id,
                    self.item.name,
                    self.wholesale_price,
                    self.quantity,
                    self.acqusition_date)

    def __repr__(self):
        """Print User when called in python repl."""
        return '<{}>'.format(self.__str__())


class Category(BASE):
    """Links an item to a category."""

    __tablename__ = 'categories'

    # Columns
    id = Column(Integer, Sequence('item_cat_id'), primary_key=True)
    name = Column(String(50), nullable=False)

    # Relationships
    # items via backref

    def __init__(self, *args, **kwargs):
        """Init magic method."""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """Print User when cast as a string."""
        return 'Category(id={}, name={})'.format(
            self.id,
            self.name)

    def __repr__(self):
        """Print User when called in python repl."""
        return '<{}>'.format(self.__str__())


class ItemCategory(BASE):
    """Links an item to a category."""

    __tablename__ = 'item_categories'

    # Columns
    id = Column(Integer, Sequence('item_cat_id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    cat_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    # Relationships
    item = relationship('Item', foreign_keys=item_id, backref='categories')
    category = relationship('Category', foreign_keys=cat_id, backref='items')

    # Constraints
    __table_args__ = (UniqueConstraint('item_id', 'cat_id', name='cat_unique'))

    def __init__(self, *args, **kwargs):
        """Init magic method."""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """Print User when cast as a string."""
        return 'ItemCategory(id={}, item_id={}, cat_id={})'.format(
            self.id,
            self.item_id,
            self.cat_id)

    def __repr__(self):
        """Print User when called in python repl."""
        return '<{}>'.format(self.__str__())


class Transaction(BASE):
    """Links an item to a category."""

    __tablename__ = 'transactions'

    # Columns
    id = Column(Integer, Sequence('item_cat_id'), primary_key=True)
    code = Column(String(10), nullable=False)
    time = Column(DateTime, nullable=False)
    payment_method = Column(String(10), nullable=False)
    tax_rate = Column(DECIMAL)
    subtotal = Column(Integer)
    tax_amount = Column(Integer)
    total = Column(Integer)

    # Relationships
    # items via backref

    def __init__(self, *args, **kwargs):
        """Init magic method."""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """Print User when cast as a string."""
        return 'Transaction(id={}, tran_code={}, tran_time={})'.format(
            self.id,
            self.code,
            self.time)

    def __repr__(self):
        """Print User when called in python repl."""
        return '<{}>'.format(self.__str__())


class TransactionItem(BASE):
    """Links an item to a category."""

    __tablename__ = 'transaction_items'

    # Columns
    id = Column(Integer, Sequence('item_cat_id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    tran_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)

    # Relationships
    item = relationship('Item', foreign_keys=item_id, backref='tran_items')
    transactions = relationship(
        'Transaction', foreign_keys=tran_id, backref='tran_items')

    def __init__(self, *args, **kwargs):
        """Init magic method."""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """Print User when cast as a string."""
        return 'FIFOItem(id={}, tran_code={}, tran_time={})'.format(
            self.id,
            self.code,
            self.time)

    def __repr__(self):
        """Print User when called in python repl."""
        return '<{}>'.format(self.__str__())
