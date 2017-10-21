from django.contrib import admin
from .models import Customer, Transaction, TransactionItem


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_code', 'time', 'payment_method', 'tax_rate', 'subtotal', 'tax_amount', 'total', 'customer')

    class Meta:
        model = Transaction


class TransactionItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'transaction')

    class Meta:
        model = TransactionItem


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email_address')

    class Meta:
        model = Customer

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(TransactionItem, TransactionItemAdmin)
admin.site.register(Customer, CustomerAdmin)
