from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RestaurantOwnerProfileForm, RestaurantForm, CategoryForm, MenuItemForm
from .models import RestaurantOwnerProfile, Restaurant, Category, MenuItem
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings
# Handle AJAX POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

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
    section = request.GET.get('section') # get section from query
    try:
        restaurant = Restaurant.objects.get(owner=request.user)
    except Restaurant.DoesNotExist:
        restaurant = None
    form = CategoryForm()
    categories = []
    if restaurant and section == 'item-category':
        categories = Category.objects.filter(restaurant=restaurant)
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name'].capitalize()
                if Category.objects.filter(name=name, restaurant=restaurant).exists():
                    messages.error(request, f"You have already added '{name}' category.")
                else:
                    category = form.save(commit=False)
                    category.name = name
                    category.restaurant = restaurant
                    category.save()
                    return redirect(f'{request.path}?section=item-category') # only redirect after success
    return render(request, 'restaurants/dashboard.html', {
        'restaurant': restaurant,
        'form': form,
        'categories': categories,
        'section': section})
    
@login_required
def delete_category_view(request, category_id):
    try:
        restaurant = Restaurant.objects.get(owner=request.user)
    except Restaurant.DoesNotExist:
        return redirect('restaurants:dashboard-view-page')
    category = get_object_or_404(Category, id=category_id, restaurant=restaurant)
    category.delete()
    return redirect(f'/restaurants/dashboard/?section=item-category')

@login_required
def category_items_view(request, category_id):
    restaurant = Restaurant.objects.get(owner=request.user)
    category = get_object_or_404(Category, id=category_id, restaurant=restaurant)
    items = MenuItem.objects.filter(category=category)
    form = MenuItemForm()
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            dish_name = form.cleaned_data['dish_name'].capitalize()
            if MenuItem.objects.filter(dish_name=dish_name, category=category).exists():
                messages.error(request, f"You have already added '{dish_name}' in '{category.name}'.")
            else:
                item = form.save(commit=False)
                item.dish_name = dish_name
                item.category = category
                item.save()
                messages.success(request, 'You have entered item details successfully.')
                return redirect('restaurants:menu-item-page', category_id=category.id)
    return render(request, 'restaurants/menu_items.html', {
        'category': category,
        'items': items,
        'form': form
    })

@login_required
def update_availability(request):
    item_id = request.POST.get('item_id')
    is_available = request.POST.get('is_available') == 'true'
    try:
        item = MenuItem.objects.get(id=item_id)
        item.is_available = is_available
        item.save()
        return JsonResponse({'status': 'success'})
    except MenuItem.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)

@login_required
def all_menu_items_view(request):
    restaurant = Restaurant.objects.get(owner=request.user)
    categories = Category.objects.filter(restaurant=restaurant)
    all_items = MenuItem.objects.filter(category__restaurant=restaurant)
    return render(request, 'restaurants/all_items.html', {
        'categories': categories,
        'all_items': all_items
    })

@login_required
def delete_item_view(request, item_id):
    dish_name = get_object_or_404(MenuItem, id=item_id)
    category_id = dish_name.category.id
    dish_name.delete()
    return redirect('restaurants:menu-item-page', category_id=category_id)