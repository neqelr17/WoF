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
    id = Column(Integer, primary_key=True)
    sku = Column(String)
    upc = Column(Integer)
    name = Column(String)
    retail_price = Column(DECIMAL)
    manufacturer = Column(String)
    quantity = Column(Integer)

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


class WholesaleItem(BASE):
    """Item meta that contains cost of quantities purchased.

    Will be consumed using FIFO.
    """

    __tablename__ = 'wholesale_items'

    # Columns
    id = Column(Integer, primary_key=True)
    price = Column(DECIMAL)
    quantity = Column(Integer)
    acqusition_date = Column(DateTime)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)

    # Relationships
    item = relationship(
        'Item', foreign_keys=item_id, backref='wholesale_items')

    def __init__(self, *args, **kwargs):
        """Init magic method."""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """Print User when cast as a string."""
        return ('WholesaleItem(id={}, item={}, price={},'
                ' quantity={}, date={})').format(
                    self.id,
                    self.item.name,
                    self.price,
                    self.quantity,
                    self.acqusition_date)

    def __repr__(self):
        """Print User when called in python repl."""
        return '<{}>'.format(self.__str__())


class Category(BASE):
    """Links an item to a category."""

    __tablename__ = 'categories'

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String())

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
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    item_id = Column(Integer, ForeignKey('items.id'))

    # Relationships
    item = relationship('Item', foreign_keys=item_id, backref='categories')
    category = relationship('Category', foreign_keys=category_id, backref='items')

    # Constraints
    __table_args__ = (UniqueConstraint('item_id', 'category_id'),)

    def __init__(self, *args, **kwargs):
        """Init magic method."""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """Print User when cast as a string."""
        return 'ItemCategory(id={}, item_id={}, category_id={})'.format(
            self.id,
            self.item_id,
            self.category_id)

    def __repr__(self):
        """Print User when called in python repl."""
        return '<{}>'.format(self.__str__())


class Customer(BASE):
    """Customer has to be linked to a transaction."""

    __tablename__ = 'customers'

    # Columns
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    email_address = Column(String)

    # Relationships
    # transactions via backref

    def __init__(self, *args, **kwargs):
        """Init magic method."""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """Print User when cast as a string."""
        return 'Customer(id={}, first_name={}, last_name={}, phone_number{})'.format(
            self.id,
            self.first_name,
            self.last_name,
            self.phone_number)

    def __repr__(self):
        """Print User when called in python repl."""
        return '<{}>'.format(self.__str__())


class Transaction(BASE):
    """Links an item to a category."""

    __tablename__ = 'transactions'

    # Columns
    id = Column(Integer, primary_key=True)
    transaction_code = Column(String())
    time = Column(DateTime)
    payment_method = Column(String())
    tax_rate = Column(DECIMAL)
    subtotal = Column(DECIMAL)
    tax_amount = Column(DECIMAL)
    total = Column(DECIMAL)
    customer_id = Column(Integer, ForeignKey('customers.id'))

    # Relationships
    # items via backref
    relationship('Customer', foreign_keys=customer_id, backref='transactions')

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
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    transaction_id = Column(Integer, ForeignKey('transactions.id'))

    # Relationships
    item = relationship('Item', foreign_keys=item_id, backref='transactions')
    transactions = relationship(
        'Transaction', foreign_keys=transaction_id, backref='items')

    def __init__(self, *args, **kwargs):
        """Init magic method."""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """Print User when cast as a string."""
        return 'TransactionItem(id={}, item_id={}, transaction_id={})'.format(
            self.id,
            self.item_id,
            self.transaction_id)

    def __repr__(self):
        """Print User when called in python repl."""
        return '<{}>'.format(self.__str__())
