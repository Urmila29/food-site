from django.db import models
from django.contrib.auth import get_user_model
from restaurants.models import MenuItem

User = get_user_model()

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def cart_total(self):
        return sum(item.cart_total_price() for item in self.cartitem_set.all())

    def __str__(self):
        return f"{self.user.username}'s Cart - Total: ₹{self.cart_total()}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartitems")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def cart_total_price(self):
        return self.quantity * self.menu_item.price

    def __str__(self):
        return f'{self.quantity} x {self.menu_item.dish_name} = ₹{self.cart_total_price()}'
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('received', 'Received'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_order = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.dish_name} (₹{self.price_at_order})"

    def total_price(self):
        return self.quantity * self.price_at_order

class Status(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status_updates")
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.order.id} - {self.status}'   
