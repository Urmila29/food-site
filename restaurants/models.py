from django.db import models
# from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class RestaurantOwnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'restaurant'})
    food_certificate = models.FileField(upload_to='certificates/')
    is_approved = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
    
class Restaurant(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'restaurant'})    
    restaurant_name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    
    is_full_day_open = models.BooleanField(default=True)
    # Full Day Open/Close
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    # Separate morning session
    morning_open_time = models.TimeField(null=True, blank=True)
    morning_close_time = models.TimeField(null=True, blank=True)
    # Separate evening session
    evening_open_time = models.TimeField(null=True, blank=True)
    evening_close_time = models.TimeField(null=True, blank=True)

    restaurant_image = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.restaurant_name
    
class Category(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.restaurant} - {self.name}'
    
class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    dish_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)
    dish_image = models.ImageField(upload_to='dish_images/', blank=True, null=True)

    def __str__(self):
        return f'{self.dish_name} - ₹{self.price}'

