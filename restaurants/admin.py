from django.contrib import admin
from .models import RestaurantOwnerProfile, Restaurant, MenuItem, Category

@admin.register(RestaurantOwnerProfile)
class RestaurantOwnerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_approved', 'submitted_at')
    list_filter = ('is_approved',)
    search_fields = ('user__email',)
    list_editable = ('is_approved',) # You can also make is_approved editable in the list view
admin.site.register(Restaurant)
admin.site.register(MenuItem)
admin.site.register(Category)