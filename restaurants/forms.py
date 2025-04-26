from django import forms
from .models import RestaurantOwnerProfile, Restaurant, Category, MenuItem

class RestaurantOwnerProfileForm(forms.ModelForm):
    class Meta:
        model = RestaurantOwnerProfile
        fields = ['restaurant_name', 'food_certificate']

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'
        widgets = {
            'open_time': forms.TimeInput(attrs={'type': 'time'}),
            'close_time': forms.TimeInput(attrs={'type': 'time'}),
            'morning_open_time': forms.TimeInput(attrs={'type': 'time'}),
            'morning_close_time': forms.TimeInput(attrs={'type': 'time'}),
            'evening_open_time': forms.TimeInput(attrs={'type': 'time'}),
            'evening_close_time': forms.TimeInput(attrs={'type': 'time'}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['owner'].label_from_instance = lambda obj: obj.username

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'placeholder': 'Enter Category Name', 'class': 'form-control'})}

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['dish_name', 'description', 'price', 'is_available', 'dish_image']
        widget = {
            'is_available': forms.CheckboxInput(attrs={'class': 'form-cjeck-input'}),
        }