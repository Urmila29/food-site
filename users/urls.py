from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup_view, name='signup-page'),
    path('login/', views.CustomLoginView.as_view(), name='login-page'),
    path('profile/', views.profile_view, name='profile-page'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout-page'),
    path('forgot-password/', views.forgot_password_view, name='forgot-password-page'),
    path('verify-otp/', views.verify_otp_view, name='verify-otp-page'),
    path('reset-password/', views.reset_password_view, name='reset-password-page'),
]
