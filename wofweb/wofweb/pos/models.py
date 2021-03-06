from django.db import models

from inventory import models as inventory_models
from django.core.validators import RegexValidator


class Customer(models.Model):
    """Custotmer model to link to transactions."""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=False, unique=True)
    email_address = models.EmailField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta():
        managed = True
        db_table = 'customers'
        app_label = 'pos'
        # ordering = ['name']


class Transaction(models.Model):
    """Sales transaction."""

    customer = models.ForeignKey(Customer, related_name='transactions')
    transaction_code = models.CharField(max_length=10)
    time = models.DateTimeField()
    payment_method = models.CharField(max_length=10)
    tax_rate = models.DecimalField(decimal_places=2, max_digits=6)
    subtotal = models.DecimalField(decimal_places=2, max_digits=6)
    tax_amount = models.DecimalField(decimal_places=2, max_digits=6)
    total = models.DecimalField(decimal_places=2, max_digits=6)

    def __str__(self):
        return self.tran_id

    class Meta():
        managed = True
        db_table = 'transactions'
        app_label = 'pos'
        ordering = ['-time']


class TransactionItem(models.Model):
    """Items sold in an transaction."""

    item = models.ForeignKey(inventory_models.Item, related_name='transactions')
    transaction = models.ForeignKey(Transaction, related_name='items')

    def __str__(self):
        return self.item.name

    class Meta():
        managed = True
        db_table = 'transaction_items'
        app_label = 'pos'
        # ordering = ['name']
