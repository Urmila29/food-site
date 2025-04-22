from django.db import models
from django.contrib.auth.models import AbstractUser
from users.validators import username_validator, email_validator

# Customize the user fields and behavior: Email - based login | User Roles (Customer, Restaurant Owner) | Extra info like phone & address
class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant Owner'),
    )
    # Custom username with space allowed, and not unique
    username = models.CharField(max_length=150, unique=False, validators=[username_validator])
    # Email: must be unique and validated
    email = models.EmailField(unique=True, validators=[email_validator])
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField()
    # This tells Django to use email as the Login field
    USERNAME_FIELD = 'email' # important
    REQUIRED_FIELDS = ['username', 'phone', 'address', 'user_type'] # or any other required fields
    def __str__(self):
        return self.email
