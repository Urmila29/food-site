from django.urls import path
from .views import register_restaurant_view, restaurant_details_view, dashboard_view, delete_category_view, category_items_view, all_menu_items_view

app_name = 'restaurants'

urlpatterns = [
    path('register-restaurant/', register_restaurant_view, name='register-restaurant-page'),
    path('restaurant-details/', restaurant_details_view, name='restaurant-details-page'),
    path('dashboard/', dashboard_view, name='dashboard-view-page'),
    path('delete-category/<int:category_id>/', delete_category_view, name='delete-category-page'),
    path('category/<int:category_id>/items/', category_items_view, name='menu-item-page'),
    path('all-items/', all_menu_items_view, name='all-item-page'),
]