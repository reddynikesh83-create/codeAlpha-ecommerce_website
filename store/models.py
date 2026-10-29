from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Audio', 'Audio & Sound'),
        ('Wearables', 'Wearables & Smartwatches'),
        ('Accessories', 'Accessories & Gadgets'),
        ('Home & Office', 'Home & Office'),
    ]

    name = models.CharField(max_length=200, help_text="Product name")
    description = models.TextField(help_text="Detailed product description")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in USD")
    image = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Uploaded product image")
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Direct external image URL for sample products")
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Electronics')
    stock = models.PositiveIntegerField(default=10, help_text="Available stock quantity")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5, help_text="Average customer rating (e.g., 4.8)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} (${self.price})"

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def display_image(self):
        """Returns uploaded image url if available, else external image_url, else fallback placeholder."""
        if self.image:
            try:
                return self.image.url
            except Exception:
                pass
        if self.image_url:
            return self.image_url
        return "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600&auto=format&fit=crop&q=80"


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.full_name} (${self.total_amount})"

    @property
    def total_items_count(self):
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_items')
    product_name = models.CharField(max_length=200, default='Product')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product_name} in Order #{self.order.id}"

    @property
    def line_total(self):
        return Decimal(str(self.price)) * Decimal(str(self.quantity))
