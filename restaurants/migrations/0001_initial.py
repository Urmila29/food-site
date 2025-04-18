# Generated by Django 5.2 on 2025-04-18 12:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish_name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('is_available', models.BooleanField(default=True)),
                ('dish_image', models.ImageField(blank=True, null=True, upload_to='dish_images/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.category')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant_name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=15)),
                ('is_full_day_open', models.BooleanField(default=True)),
                ('open_time', models.TimeField(blank=True, null=True)),
                ('close_time', models.TimeField(blank=True, null=True)),
                ('morning_open_time', models.TimeField(blank=True, null=True)),
                ('morning_close_time', models.TimeField(blank=True, null=True)),
                ('evening_open_time', models.TimeField(blank=True, null=True)),
                ('evening_close_time', models.TimeField(blank=True, null=True)),
                ('restaurant_image', models.ImageField(blank=True, null=True, upload_to='restaurant_images/')),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.OneToOneField(limit_choices_to={'user_type': 'restaurant'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant'),
        ),
        migrations.CreateModel(
            name='RestaurantOwnerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_certificate', models.FileField(upload_to='certificates/')),
                ('is_approved', models.BooleanField(default=False)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(limit_choices_to={'user_type': 'restaurant'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
