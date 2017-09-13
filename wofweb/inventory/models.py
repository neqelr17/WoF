"""Models that describe the inventory."""
from django.db import models


class Item(models.Model):
    """An Item describes characteristics of an item."""

    sku = models.CharField(max_length=8, unique=True)
    upc = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)
    retail_price = models.DecimalField(decimal_places=2, max_digits=6)
    manufacturer = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)

    class Meta():
        managed = True
        db_table = 'items'
        app_label = 'inventory'
        ordering = ['name']


class WholesaleItem(models.Model):
    """A WholesaleItem describes the cost group and counts of an item."""

    item = models.ForeignKey(Item, related_name='wholesale')
    price = models.DecimalField(decimal_places=2, max_digits=6)
    quantity = models.IntegerField()
    acqusition_date = models.DateTimeField()

    class Meta():
        managed = True
        db_table = 'wholesale_items'
        app_label = 'inventory'
        ordering = ['acqusition_date']


class Category(models.Model):
    """Describes categories that an item can belong to."""

    name = models.CharField(max_length=50, unique=True)

    class Meta():
        managed = True
        db_table = 'categories'
        app_label = 'inventory'
        ordering = ['name']


class ItemCategory(models.Model):
    """Links items to many categories."""

    item = models.ForeignKey(Item, related_name='categories')
    category = models.ForeignKey(Category, related_name='items')

    class Meta():
        managed = True
        db_table = 'item_categories'
        app_label = 'inventory'
        ordering = ['id']
        unique_together = (('item', 'category'))


class Transaction(models.Model):
    """Sales transaction."""

    tran_id = models.CharField(max_length=10)
    time = models.DateTimeField()
    payment_method = models.CharField(max_length=10)
    tax_rate = models.DecimalField(decimal_places=2, max_digits=6)
    subtotal = models.DecimalField(decimal_places=2, max_digits=6)
    tax_amount = models.DecimalField(decimal_places=2, max_digits=6)
    total = models.DecimalField(decimal_places=2, max_digits=6)

    class Meta():
        managed = True
        db_table = 'transactions'
        app_label = 'inventory'
        ordering = ['-time']


class TransactionItem(models.Model):
    """Items sold in an transaction."""

    item = models.ForeignKey(Item, related_name='transaction_items')
    transaction = models.ForeignKey(Transaction, related_name='transaction_items')

    class Meta():
        managed = True
        db_table = 'item_tansactions'
        app_label = 'inventory'
        # ordering = ['name']
