"""Models that describe the inventory."""
from django.db import models


class Item(models.Model):
    """An Item describes characteristics of an item."""

    sku = models.CharField(max_length=8, unique=True)
    upc = models.BigIntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=50)
    retail_price = models.DecimalField(decimal_places=2, max_digits=6)
    manufacturer = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

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
    roosters = models.BooleanField()

    def __str__(self):
        return self.item.name

    class Meta():
        managed = True
        db_table = 'wholesale_items'
        app_label = 'inventory'
        ordering = ['acqusition_date']


class Category(models.Model):
    """Describes categories that an item can belong to."""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta():
        managed = True
        db_table = 'categories'
        app_label = 'inventory'
        ordering = ['name']
        verbose_name_plural = 'Categories'


class ItemCategory(models.Model):
    """Links items to many categories."""

    item = models.ForeignKey(Item, related_name='categories')
    category = models.ForeignKey(Category, related_name='items')

    def __str__(self):
        return self.item.name

    class Meta():
        managed = True
        db_table = 'item_categories'
        app_label = 'inventory'
        ordering = ['id']
        unique_together = (('item', 'category'))
        verbose_name_plural = 'Item categories'
