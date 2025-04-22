'''
#- Step1: Set Up Project & Apps
#_  Task                    Description
    Create Django Project   fooddelivery
    Create Apps             users, restaurants, orders, core
#! cmd
python -m venv fsenv
fsenv\Scripts\activate
pip install django
pip install psycopg2-binary
pip install djangorestframework
pip install pillow
django-admin startproject foodsite .
python manage.py startapp users
python manage.py startapp restaurants
python manage.py startapp orders
#! pgAdmin 4
Database/Create/Database/fsdb
#! settings.py
INSTALLED_APP = [
    'rest_framework',
    'users',
    'restaurants',
    'orders',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fsdb',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
#! cmd
python manage.py migrate
python manage.py runserver #/ The install worked successfully! Congratulations!
python manage.py createsuperuser
Username: admin
Email: admin@test.com
Password: admin@123 #/ Superuser created successfully.
#- Step2: Create Models : We want to create a user system with roles (customer or restaurant owner)
#_  App         Models
    users       Custom User (email login, name, address, phone, role: customer/restaurant)
    restaurants Restaurants, MenuItem, Category
    orders      Cart, CartItem, Order, OrderItem, Status
#_ users       Custom User (email login, name, address, phone, role: customer/restaurant)
#! users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from users.validators import username_validator, email_validator
#/ Customize the user fields & behavior: Email - based login | User Roles (Customer, Restaurant Owner) | Extra info like phone & address
class CustomUser(AbstractUser):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant Owner'),
    )
    #/ Username : space allowed, and not unique
    username = models.CharField(max_length=150, unique=False, validators=[username_validator])
    #/ Email : must be unique & valaidated
    email = models.EmailField(unique=True, validators=[email_validator])
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField()
    #/ Tells Django to use email as the Login field
    USERNAME_FIELD = 'email #/ important
    REQUIRED_FIELDS = ['username', 'phone', 'address', 'user_type'] #/ or any other required fielsds
    def __str__(self):
        return self.email
#! settings.py
AUTH_USER_MODEL = 'users.CustomUser'
#! users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'address', 'user_type', 'password1', 'password2']
class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(#/ Overrride 'username' field label & type
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
    )
#! users/validators.py
from django.core.validators import RegexValidator, EmailValidator
#/ Username: Only Letters, Digits, & Spaces allowed
username_validator = RegexValidator(
    regex=r'^[A-Za-z0-9 ]+$',
    message="Username can contain only letters, digits, & spaces.",
    code='invalid_username'
)
#/ Email: standard Django email validator (already ensures proper format)
email_validator = EmailValidator(
    message="Enter a valid email address."
)
#! users/admin.py : Register the model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
class CustomUserAdmin(UserAdmin): #/ Inherits admin functionality (search, filters, user permissions)
    model = CustomUser
    list_display = ['username', 'email', 'user_type', 'is_staff'] #/ which fields shown in the admin list view (table of users)
admin.site.register(CustomUser, CustomUserAdmin) #/ User CUA to manage CU objects in the admin panel
#! users/views.py
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import login #/ auto-login users after signup
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from .froms import CustomUserCreationForm, EmailLoginForm

def home_view(request):
    return render(request, 'users/index.html')

def signup_view(request)L
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.dave()
            email = form.cleaned_data.get('email')
            login_url = reverse('users:login-page')
            messages.success(request, 'Signup successfull! Please log in.')
            return redirect(f"{login_url}?email={email}")
        else:
            messages.error(request, 'Signup failded. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/signup.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = EmailLoginForm #/ Uses our custom login form

    def form_valid(self, form):
        messages.success(self.request, 'Logged in successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Login failed. Please try again.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('users:profile-page')
#! users/urls.py : Configuration
from django.urls import path
from django.contrib.auth import views as auth_views #/ auth_views : built-in (login, logout, password reset)
from . import views
app_name = 'users' #/ namespace : helps you reference these URLs : {% url 'users:login-page' %}
urlpatterns = [
    path('signup/', views.signup_views, name='signup-page'),
    path('login/', views.CustomLoginView.as_view(), name='login-page'), #/ .as_view() method turns your class into a usable view function.
    path('profile/', views.profile_view, name='profile-page'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout-page'), #/ LogoutView : logs out the user using Django's default logoutview
]
#! urls.py
from django.contrib import admin
from django.urls import path, include
from users.views import home_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')), #/ namespace='users' : differentiate the URLs if multiple apps use the same view names. : <a href="{% url 'users:login-page' %}">Login</a>
    path('', home_view, name='home-page'),
]
#! settings.py
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #/ __file__ : settings.py | build paths dynamically
STATIC_URL = 'foodsite/static/'
STATICFILES_DIRS = [ #/ tells Django where to look for static files outside of app directories.
    os.path.join(BASE_DIR, 'foodsite/static'),
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'foodsite', 'templates')], #/ tells Django where to look for project-level templates (not tied to any specific app).
        'APP_DIRS': True,
    }
]
#! HTML pages : Login, Signup, Profile, Logout, Home, Header, Footer
#! foodsite/templates/home.html : Devide it in header, footer
{% loas static %} #/ should be 1st line : to use : {% static 'path/to/file' %} for CSS, JS, images, etc.
{% include 'header.html' %} #/ includes another HTML file
{% block content %}
{% endblock %}
<main>
    <section>
        {% if messages and user.is_authenticated %}
            <ul class="messages">
                {% for message in messages %}
                    <li class="{{ message.tags }}">{{ message }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </section>
    #/ . . .
{% include 'footer.html' %}
{% block footer %}
{% endblock %}
</body>
</html>
#! foodsite/templates/header.html : apply static, set data to visible for logged in users or not logged in users
{% load static %}
#/ . . .
    <head>
        <link rel="stylesheet" href="{% static 'assets/css/style.css' %}"> #/ apply static to css file
    </head>
    <body>
        <header>
            {% if user.is_authenticated %}
                <a href="{% url 'home-page' %}">
                    <img src="{% static 'assets/images/logo.png' %}" alt="FoodSite logo" height="100">
                </a>
            {% else %}
                <h1><a href="{% url 'home-page' %}">FoodSite</a></h1>
            {% endif %}
#/ . . .
            <div class="auth-cart">
                <a href="#cart">🛒 Cart</a>
                {% if user.is_authenticated %}
                    <form method="POST" action="{% url 'users:logout-page' %}">
                        {% csrf_token %} #/ Cross-Site Request Forgery : This token protects your form from malicious attacks.
                        <button type="submit" class="logout-btn">Logout</button>
                    </form>
                    <a href="{% url 'users:profile-page' %}">Profile</a>
                {% else %}
                    <a href="{% url 'users:login-page' %}">Login</a>
                {% endif %}
            </div>
#! foosite/templates/footer.html
#! foodsite/static/assets/css/styles.css
#! users/templates/users/login.html
{% include 'header.html' %}
{% block content %}
    <h2>Login</h2>
    {% if messages %}
        {% for message in messages %}
            <li class="{{ message.tags }}>{{ message }}</li>
        {% endfor %}
    {% endif %}
    <form method="POST" action="{% url 'users:login-page' %}">
        {% csrf_token %}
        {{ form.as_p }} #/ Template Variable : used to render a Django form inside your HTML and it: Renders each field of the form wrapped in a <p> tag
        <button type="submit">Login</button>
    </form>
    <p>Don't have an account? <a href="{% url 'users:signup-page' %}" class="highlight-link">Register here...</a></p>
{% endblock %}
{% include 'footer.html' %}
#! users/templates/users/signup.html
{% if messages %}
    {% for message in messages %}
        <li class="{{ message.tags }}">{{ message }}</li>
    {% endfor %}
{% endif %}
<form method="POST" action="{% url 'users:signup-page' %}">
    {% csrf_token %}
    {{ form.as_p }}
    {% if form.errors %}
        {% for field in form %}
            {% for error in field.errors %}
                <li>{{ field.label }}: {{ error }}</li>
            {% enfor %}
        {% endfor %}
        {% for error in form.non_field_errors %}
            <li>{{ error }}</li>
        {% endfor %}
    {% endif %}
    <button type="submit">Register</button>
</form>
<p>Already have an account? <a href="{% url 'users:login-page' %}" class="highlight-link">Login here...</a></p>
#! users/templates/users/profile.html
{% if messages %}
    {% for message in messages %}
        <li class="{{ message.tags }}">{{ message }}</li>
    {% endfor %}
{% endif %}
<h2>Welcome, {{ user.username }}</h2>
<table>
    <tr><th>Usename</th><td>{{ user. username }}</td></tr>
    <tr><th>Email</th><td>{{ user.email }}</td></tr>
    <tr><th>Phone</th><td{{ user.phone }}></td></tr>
    <tr><th>Address</th><td>{{ user.address }}</td></tr>
</table>
#_ Forgot Password, Verify OTP, Reset Password
#! users/forms.py : Setup
form django import forms
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6)
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    def clean(self): #/ Custom validation: Cross field validation (When multiple fields depend on each other)
        cleaned_data = super().clean() #/ gets all cleaned (validated) data after field-level validation
        if cleaned_data.get('new_password') != cleaned_data.get('confirm_password):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
#! users/views.py
import random
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.conf import settings
from .forms import ForgotPasswordForm, OTPVerificationForm, ResetPasswordForm
User = get_user_model()
def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid(): #/ Checks if the email is valid
            email = form.cleaned_data['email'] #/ Extracts the cleaned (sanitized) email
            try:
                user = User.objects.get(email=email)
                otp = str(random.randint(100000, 999999))
                request.session['reset_email'] = email #/ Saves OTP and email to Django's session: This data is stored temporarily per user (even if browser is closed), Used later in OTP verification step.
                request.session['reset_otp'] = otp
                send_mail( #/ sends a simple email with OTP using Django's send_mail(), settings.DEFAULT_FROM_EMAIL must be configured in settings.py
                    subject='Your OTP for password Reset',
                    message=f'Your OTP is: {otp}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False
                )
                return redirect('users:verify-otp-page')
            except User.DoesNotExist:
                messages.error(request, 'No account found with this email.')
    else:
        from = ForgotPasswordForm()
    return render(request, 'users/forgot_password.html', {'form': form})
def verify_otp_view(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            input_otp = form.cleaned_data['otp'] #/ extracts the cleaned OTP value the user entered
            session_otp = request.session.get('reset_otp') #/ Fetches correct OTP from session. 
            if input_otp == session_otp:
                return redirect('users:reset-password-page')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPVerificationForm()
    return render(request, 'users/verify_otp.html', {'form': form})
def reset_password_view(request):
    email = request.session.get('reset_email') #/ you stored user's email in session during forgot password step: now you retrieve it to identify which user's password to reset.
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST) #/ create a form instance with submitted data(new password+confirm password)
        if form.is_valid(): #/ ensures both fields are filled & passwords matched
            password = form.cleaned_data['new_password'] #/ extract validated new password
            try:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                messages.success(request, 'Password updated successfully! You can now log in.')
                request.session.flush() #/ cleare session data
                return redirect('users:login-page')
            except User.DoesNotExist:
                messages.error(request, 'User not found. Please try again.')
    else:
        form = ResetPasswordForm()
    return render(request, 'users/reset_password.html', {'form': form})
#! users/urls.py
path('forgot-password/', views.forgot_password_view, name='forgot-password-page'),
path('verify-otp/', views.verify_otp_view, name='verify-otp-page'),
path('reset-password/', views.reset_password_view, name='reset-password-page'),
#! users/templates/users/forgot_password.html
<h2>Forgot Password</h2>
{% if messages %}
    {% for message in messages %}
        <li class="{{ message.tas }}">{{ message }}</li>
    {% endfor %}
{% endif %}
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Send OTP</button>
</form>
#! users/templates/users/verify_otp.html
<h2>Enter OTP</h2>
{% if messages %}
    {% for message in messages %}
        <li class="{{ message.tags }}">{{ message }}</li>
    {% endfor %}
{% endif %}
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Verify</button>
</form>
#! users/templates/users/reset_password.html
<h2>Reset Your Password</h2>
{% if messages %}
    {% for message in messages %}
        <li class="{{ message.tags }}">{{ message }}</li>
    {% endfor %}
{% endif %}
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Update Password</button>
</form>
#! settings.py : Ensures email settings are configured (Simple Mail Transfer Protocol)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' #/ Tells Django to use SMTP protocol to send emails.
EMAIL_HOST = 'smtp.gmail.com' #/ This is Gmail SMTP server address
EMAIL_PORT = 587 #/ Used for TLS (encrypted) connections
EMAIL_USE_TLS = True #/ Enables TLS encryption, which is necessary for secure communication with Gmail
EMAIL_HOST_USER = 'daforpreactice@gmail.com' #/ This account must allow SMTP access (usually through an App Password if 2FA is enabled)
EMAIL_HOST_PASSWORD = 'qtryhqmsliqpbkxz' #/ Use app password if 2fa is on : Generated from your Google Account > Security > App Passwords
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
#! restaurants/models.py
#_ restaurants: Model(RestaurantOwnerProfile, Restaurant, Category, MenuItem)
#- RestaurantOwnerProfile : user, food_certificate, is_approved, submitted_at
#- Restaurant : owner, restaurant_name, address, phone, opening_time, closing_time, image, created_at
#- Category : restaurant, name
#- MenuItem : category, name, description, price, image, is_available
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
class RestaurnatProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'restaurant'}) #/ Only restaurant-type users allowed
    restaurant_name = models.CharField(max_length=100)
    food_certificate = models.FileField(upload_to='certificates/') #/ Upload cerificate file (PDF, image etc.)
    is_approved = models.BooleanField(default=False) #/ Admin will manually approve this
    submitted_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.email #/ Easy display in admin panel or admin page
class Restautant(models.Model):
    owner = models.OneToOneField(User, on_delete=CASCADE, limit_choices_to={'user_type': 'restautant'})
    address = models.TextField()
    phone = models.CharField(max_length=15)
    description = models.TextField()
    is_full_day_open = models.BooleanField(default=False) #/ if True: open_time, close_time
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    morning_open_time = models.TimeField(null=True, blank=True) #/ if False: seperate morning session
    morning_close_time = models.TimeField(null=True, blank=True)
    evening_open_time = models.TimeField(null=True, blank=True) #/ if False: seperate evening session
    evening_close_time = models.TimeField(null=True, blank=True)
    restaurant_image = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.restaurant_name
class Category(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu_name = models.CharField(max_lenght=100)
    def __str__(self):
        return f'{self.restaurant} - {self.menu_name}'
class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    dish_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalsField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)
    dish_image = models.ImageField(upload_to='dish_images/', blank=True, null=True)
    def __str__(self):
        return f'{self.dish_name} - ₹{self.price}'
#! orders/models.py
#_ orders: Cart(User's current cart), CartItem(Individual food items in the cart), Order(A placed order), OrderItem(Items in the order), Status(Status updates of the order (Optional but useful))
#- Cart: user, return username's cart, total of cart
#- CartItem: cart, menu_item, quantity, return display, quantity x dish_name, total of quantity * dish_price
#- Order: STATUS_CHOICES, user, status, created_at, updated_at, total_amount, return "order id by username"
#- OrderItem: order, menu_item, quantity, price_at_order, return "quantity x dish_name", quantity * price_at_order
#- Status: order, updated_at, status, return "order - status"
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
        return f"{self.quantity} x {self.menu_item.dish_name} = ₹{self.cart_total_price()}"
class Order(models.Model):
    STATUS_CHOICES = (
        ('received', 'Received'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="received")
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
        return f"Order #{self.order.id} - {self.status}"
#! CMD
python manage.py makemigrations restaurants, orders
python manage.py migrate
#! Github
1. Download git : https://git-scm.com/download/win
2. The download will start automatically. After it finishes, run the installer.
3. In the installation steps:
    Keep default options as they are.
    When you see the option "Adjusting your PATH environment", make sure this is selected:
✅ "Git from the command line and also from 3rd-party software"
4. Finish the installation.
5. cmd: git --version #/ git version 2.49.0.windows.1
#! Steps to updating code in GitHub without losing folder
#* 1. Create a local project folder
mkdir myproject
cd myproject
#* 2. Set up a Python Virtual Environment
python -m venv venv
venv\Scripts\activate
#* 3. Initialize Git
git init
#/ Initialized empty Git repository in D:/Python_UR/Portfolio3/.git/
#* 4. Create a .gitignore File : Copy below code & Paste it (this file tells Git what not to track)
code .gitignore
#/ Virtual Environment
venv/
#/ Python cache
__pyache__/
*.pyc
#/ Environment Variables
.env
.env.*
#/ VS Code
.vscode/
#/ SQLite DB
*.sqlite3
#/ Static/media files (if Django) : Best way
static/
media/
#/ Ignore static & media folders from 'myproject/'
myproject/static/
myproject/media/
#* 5. Create your Project : main.py, app/, templates/, etc.
#* 5. You can also install dependencies & then freeze them:
pip install django
pip freeze > requirements.txt #/ How to use: pip install -r requirements.txt
#* 6. Add & Commit Your Code to Git
git status #/ 1st, check what Git sees
#!        .gitignore
#!        db.sqlite3
#!        foodsite/
#!        manage.py
#!        orders/
#!        restaurants/
#!        static/
#!        steps.py
#!        templates/
#!        users/
git add . #/ then add your files
git commit -m "1. Set Up Project & Apps | 2. Created Models"
#_ If FATAL Error: Who you are?
git config --global user.name "Urmila Sarvaiya"
git config --global user.email "sanurmi0129@gmail.com"
#_ Want to check if it worked?
got config --global --list #/ user.name= | user.email=
#_ Now: Re-run your commit command
git commit -m "1. Set Up Project & Apps | 2. Created Models"
#* 7. Create GitHub Repository
Go to https://github.com
Click + > New Repository
Fill in:
    Repository name(food-site)
    Set poblic/private
    DO NOT initialize with README/anything (we already have local files)
    Click create repository
#_ GitHub will show you a link like this:
#/ https://github.com/Urmila29/food-site.git
Copy it.
#* 8. Connect Local Git to GitHub & Push
git remote add origin https://github.com/Urmila29/food-site.git
git branch -M main
git push -u origin main #!(rejected) main > main (fetch first) error: failed to push some refs to
git pull origin main --rebase #/ error: Commit or stash them
git add .
git commit -m "Commit/stash"
git pull origin main --rebase
git push -u origin main #/ Enumerating objects: 93 done.
#_ Now: your code is on GitHub!
#* 9. Add more code / Update Existing Code
git status
#!        modified:   steps.py #/ see what's changed
git add . #/ add changes
gir commit -m "Step.py changed"
git push origin main #/ push your local main brach to remote main branch
#* Bonus: If you work on another PC : want to pull your code
git clone https://github.com/your-username/localproject.git
cd myproject
python -m venv venv
venv\Scripts\activate #/ then install from requirements
pip install -r requirements.txt
#/ now you are ready to continue working!
#_ SUMMARY OF KEY GIT COMMANDS
#! Command                      What it does
#- git init                     Start Git in your folder
#- git add .                    Stage changes
#- git commit -m "message"      Save a snapshot
#- git remote add origin <url>  Connect to GitHub
#- git push origin main         Upload code
#- git pull origin main         Download code
#- git status                   See what's changed
#- git clone <url>              Download whole repo

#- Step3: Views & Templates
Home Page: list all restaurants
Restaurant detail page: menu, info, ratings
Cart Page: Add/Remove/Update items
Checkout page: confirm address, payment method
Orders page: View current and past orders
#! Register the models: orders/admin.py
from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem, Status
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Status)
#! restaurants/admin.py
from django.contrib import admin
from .models import RestaurantOwnerProfile, Restaurant, MenuItem, Category
#* see all restaurant registrations in the admin panel & approve them directly
@admin.register(RestaurantOwnerProfie)
class RestaurantOwnerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_approved', 'submitted_at')
    list_filter = ('is_approve',)
    search_fields = ('user__email',)
    list_editable = ('is_approved',) #/ You can also make is_approved editable in the list view
admin.site.Register(Restaurant)
admin.site.Register(MenuItem)
admin.site.Register(Category)
#! CMD: Create superuser if not stored in database: add 'admin to choices in users/models.py'
python manage.py runserver #/ https://127.0.0.1:8000/admin/
#! restaurants/forms.py : Create a Restaurant Registration Form
from django import form
from .models import RestaurantOwnerProfile
class RestaurantOwnerProfileForm(forms.ModelForm):
    class Meta:
        model = RestaurantOwnerProfile
        fields = ['food_certificate']
#! restaurants/views.py : Create a view to handle requests

#! templates/restaurants/register_restaurant.html

#! restaurants/urls.py

#! urls.py : access restaurants's urls

#! 
#- Home Page: list all restaurants
#- Restaurant detail page: menu, info, ratings
#- Cart Page: Add/Remove/Update items
#- Checkout page: confirm address, payment method
#- Orders page: View current and past orders
#! users/templates/users/verify_otp.html
#! users/templates/users/verify_otp.html

#- Step4: Authentication System
User Signup/Login using email/password
Profile dashboard (name, address, etc.)
Different user types: Customer vs Restaurant Owner
#- Step5: Order System
Add to cart
Checkout flow
Order tracking (status: recieved, preparing, out for delivery, delivered)
#- Step6: Admin Panel
Add/edit/delete restaurants & food items
Manage orders
View statistics (order per day, top-selling dishes)
#- Step7: (Optional Advanced Features)
Add search & filter for restaurants/dishes
Rating/reviews system
Mobile responsiveness
Payment gateway integration
Notifications for order status
#- Project Structure Overview
fooddelivery(Portfolio2)/
|___ fooddelivery(foodsite)/  #/ Project settings
|___ users/                   #/ Login, registration, user profiles
|___ restaurants/             #/ Restaurants & Menu
|___ orders/                  #/ Cart, Checkout, Order History
|___ templates/               #/ HTML templates
|___ static/                  #/ CSS, JS, Images

'''