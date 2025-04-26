from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('register-restaurant/', views.register_restaurant_view, name='register-restaurant-page'),
    path('restaurant-details/', views.restaurant_details_view, name='restaurant-details-page'),
    path('dashboard/', views.dashboard_view, name='dashboard-view-page'),
    path('delete-category/<int:category_id>/', views.delete_category_view, name='delete-category-page'),
    path('category/<int:category_id>/items/', views.category_items_view, name='menu-item-page'),
    path('update-availability/', views.update_availability, name='update-availability-page'),
    path('all-items/', views.all_menu_items_view, name='all-item-page'),
    path('delete-item/<int:item_id>/', views.delete_item_view, name='delete-item-page'),
]