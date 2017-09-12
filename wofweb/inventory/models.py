from django.db import models

# Create your models here.
class Item(models.Model):
    """A server represents a physical/vm server in the infrastructure."""

    sku = models.CharField(max_length=8, unique=True)
    upc = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)
    retail_price = models.DecimalField(decimal_places=2)
    manufacturer = models.CharField(max_length=50)

    class Meta():
        managed = True
        db_table = 'items'
        app_label = 'inventory'
        ordering = ['name']
