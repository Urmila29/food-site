from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import login #/ auto-login users after signup
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from .forms import CustomUserCreationForm, EmailLoginForm, ForgotPasswordForm, OTPVerificationForm, ResetPasswordForm

import random
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

# from django.db import connection
# print("Connected DB:", connection.settings_dict['NAME'])

def home_view(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            login_url = reverse('users:login-page')
            messages.success(request, 'Signup successful! Please log in.')
            return redirect(f"{login_url}?email={email}")
            # return redirect('users:login-page') # login(request, user)
            # return redirect('/')
        else:
            messages.error(request, 'Signup failed. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/signup.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                otp = str(random.randint(100000, 999999))
                request.session['reset_email'] = email
                request.session['reset_otp'] = otp
                send_mail(
                    subject='Your OTP for Password Reset',
                    message=f'Your OTP is: {otp}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False
                )
                return redirect('users:verify-otp-page')
            except User.DoesNotExist:
                messages.error(request, 'No account found with this email.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'users/forgot_password.html', {'form': form})

def verify_otp_view(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            input_otp = form.cleaned_data['otp']
            session_otp = request.session.get('reset_otp')
            if input_otp == session_otp:
                return redirect('users:reset-password-page')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPVerificationForm()
    return render(request, 'users/verify_otp.html', {'form': form})

def reset_password_view(request):
    email = request.session.get('reset_email')
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['new_password']
            try:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                messages.success(request, 'Password updated successfully! You can now log in.')
                # Clear session data
                request.session.flush()
                return redirect('users:login-page')
            except User.DoesNotExist:
                messages.error(request, 'User not found. Please try agian.')
    else:
        form = ResetPasswordForm()
    return render(request, 'users/reset_password.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = EmailLoginForm # Use our custom Login form
    
    def form_valid(self, form):
        messages.success(self.request, 'Logged in successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Login failed. Please try again.')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('users:profile-page')
