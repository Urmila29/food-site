from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RestaurantOwnerProfileForm, RestaurantForm
from .models import RestaurantOwnerProfile, Restaurant
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings

@login_required
def register_restaurant_view(request):
    try:
        restaurant = request.user.restaurant_owner
        messages.info(request, "You have already submitted a request.")
        return redirect('users:profile-page')
    except RestaurantOwnerProfile.DoesNotExist:
        if request.method == 'POST':
            form = RestaurantOwnerProfileForm(request.POST, request.FILES)
            if form.is_valid():
                restaurant = form.save(commit=False)
                restaurant.user = request.user
                restaurant.save()
                messages.success(request, "Restaurant registration request submitted successfully.")
                return redirect('users:profile-page')
        else:
            form = RestaurantOwnerProfileForm
    return render(request, 'restaurants/register_restaurant.html', {'form': form})

def send_approval_email(user):
    subject = "Restaurant Approval Status"
    message = "Congratulations! Your restaurant registration has been approved."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

@login_required
def restaurant_details_view(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.restaurant_owner_profile = request.user.restaurant_owner
            restaurant.save()
            messages.success(request, "Restaurant details updated successfully!")
            return redirect('restaurants:dashboard-view-page')
        else:
            messages.error(request, 'Add details carufully.')
    else:
        form = RestaurantForm()
    return render(request, 'restaurants/restaurant_details.html', {'form': form})

@login_required
def dashboard_view(request):
    try:
        restaurant = Restaurant.objects.get(owner=request.user)
    except Restaurant.DoesNotExist:
        restaurant = None
    return render(request, 'restaurants/dashboard.html', {'restaurant': restaurant})