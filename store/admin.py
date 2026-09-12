from django.contrib import admin
from .models import Category, Item, Delivery

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    ordering = ('name',)

class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'quantity', 'price', 'expiring_date', 'vendor'
    )
    search_fields = ('name', 'category__name', 'vendor__name')
    list_filter = ('category', 'vendor')
    ordering = ('name',)

class DeliveryAdmin(admin.ModelAdmin):
    list_display = (
        'item', 'customer_name', 'phone_number',
        'location', 'date', 'is_delivered'
    )
    search_fields = ('item__name', 'customer_name')
    list_filter = ('is_delivered', 'date')
    ordering = ('-date',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Delivery, DeliveryAdmin)