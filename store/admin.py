from django.contrib import admin
from .models import Category,Product



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name' , 'slug']
    list_filter = ['name' , 'slug']
    prepopulated_fields = {"slug" : ("name" ,)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'created_by', 'author', 'price', 'is_stock',
        'is_active', 'created', 'updated','image'
    ]

    list_filter = [
        'title',
        'author','price','is_stock',
        'is_active','created','updated',
        'category','created_by'
    ]

    prepopulated_fields = {"slug" : ("title" ,)}
