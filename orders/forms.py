from django import forms
from .models import Cart, CartItem, Order, OrderItem, Status

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
