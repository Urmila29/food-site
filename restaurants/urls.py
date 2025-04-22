from django.urls import path
from .views import register_restaurant_view, restaurant_details_view, dashboard_view

app_name = 'restaurants'

urlpatterns = [
    path('register-restaurant/', register_restaurant_view, name='register-restaurant-page'),
    path('restaurant-details/', restaurant_details_view, name='restaurant-details-page'),
    path('dashboard-page/', dashboard_view, name='dashboard-view-page'),
]