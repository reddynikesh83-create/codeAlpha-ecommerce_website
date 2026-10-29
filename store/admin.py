from django.contrib import admin
from .models import Product, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('line_total',)

    def line_total(self, instance):
        return f"${instance.line_total:.2f}"
    line_total.short_description = "Line Total"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock', 'rating', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description', 'category')
    list_editable = ('price', 'stock')
    ordering = ('-created_at',)
    fieldsets = (
        ('General Information', {
            'fields': ('name', 'category', 'description')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock', 'rating')
        }),
        ('Media', {
            'fields': ('image', 'image_url')
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'phone', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'address')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'total_amount')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product_name', 'quantity', 'price')
    list_filter = ('order__status',)
    search_fields = ('product_name', 'order__full_name', 'order__id')
