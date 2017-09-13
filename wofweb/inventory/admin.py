from django.contrib import admin
from .models import (Category,
                     Item,
                     ItemCategory,
                     Transaction,
                     TransactionItem,
                     WholesaleItem)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'upc', 'retail_price', 'manufacturer')

    class Meta:
        model = Item


admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(ItemCategory)
admin.site.register(Transaction)
admin.site.register(TransactionItem)
admin.site.register(WholesaleItem)
