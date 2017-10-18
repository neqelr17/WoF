from django.contrib import admin
from .models import (Category,
                     Item,
                     ItemCategory,
                     WholesaleItem)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

    class Meta:
        model = Category


class ItemAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'upc', 'retail_price', 'manufacturer')

    class Meta:
        model = Item


class WholesaleItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'price', 'quantity', 'acqusition_date')

    class Meta:
        model = WholesaleItem


class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('item', 'category')

    class Meta:
        model = ItemCategory


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(WholesaleItem, WholesaleItemAdmin)
