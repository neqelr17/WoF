from django.db import models
from django.core.validators import RegexValidator


from inventory import models as inventory_models


class Employee(models.Model):
    """POS using employee."""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=20)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=(
        'Phone number must be entered in the format: '
        '"+999999999". Up to 15 digits allowed.'))
    phone_number = models.CharField(
        validators=[phone_regex], max_length=15, blank=False, unique=True)
    email_address = models.EmailField()
    salt = models.CharField(max_length=20)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.user_name

    class Meta():
        managed = True
        db_table = 'employees'
        app_label = 'pos'
        # ordering = ['name']


class Customer(models.Model):
    """Custotmer model to link to transactions."""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=(
        'Phone number must be entered in the format: ',
        '"+999999999". Up to 15 digits allowed.'))
    phone_number = models.CharField(
        validators=[phone_regex], max_length=15, blank=False, unique=True)
    email_address = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta():
        managed = True
        db_table = 'customers'
        app_label = 'pos'
        # ordering = ['name']


class Transaction(models.Model):
    """Sales transaction."""

    employee = models.ForeignKey(
        Employee, related_name='employee_transactions')
    customer = models.ForeignKey(Customer, related_name='transactions')
    transaction_code = models.CharField(max_length=40, unique=True)
    time = models.DateTimeField()
    payment_method = models.CharField(max_length=10)
    tax_rate = models.DecimalField(decimal_places=2, max_digits=6)
    subtotal = models.DecimalField(decimal_places=2, max_digits=6)
    tax_amount = models.DecimalField(decimal_places=2, max_digits=6)
    total = models.DecimalField(decimal_places=2, max_digits=6)

    def __str__(self):
        return self.transaction_code

    class Meta():
        managed = True
        db_table = 'transactions'
        app_label = 'pos'
        ordering = ['-time']


class TransactionItem(models.Model):
    """Items sold in an transaction."""

    item = models.ForeignKey(
        inventory_models.Item, related_name='transactions')
    transaction = models.ForeignKey(Transaction, related_name='items')

    def __str__(self):
        return self.item.name

    class Meta():
        managed = True
        db_table = 'transaction_items'
        app_label = 'pos'
        # ordering = ['name']


class Return(models.Model):
    """A base return."""

    employee = models.ForeignKey(Employee, related_name='employee_returns')
    transaction = models.ForeignKey(Transaction, related_name='returns')
    returned_timestamp = models.DateTimeField()

    def __str__(self):
        return '{} {} {}'.format(
            self.employee, self.transaction, self.returned_timestamp)

    class Meta():
        managed = True
        db_table = 'returns'
        app_label = 'pos'


class ReturnItem(models.Model):
    """Represents an item that has been returned."""

    return_transaction = models.ForeignKey(Return, related_name='return_items')
    tran_item = models.ForeignKey(TransactionItem, related_name='returns')
    condition = models.CharField(max_length=50)

    def __str__(self):
        return self.tran_item.item.name

    class Meta():
        managed = True
        db_table = 'return_items'
        app_label = 'pos'
