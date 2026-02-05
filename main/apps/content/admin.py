from django.contrib import admin
from .models import Category, Model


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    list_filter=['name']
    search_fields = ['name', 'description']

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']
    list_filter=['name', 'category', 'price']
    search_fields = ['name', 'description']
    
