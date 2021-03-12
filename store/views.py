from django.shortcuts import render, get_object_or_404,get_list_or_404
from .models import Product,Category


def Categories(request):
    categories = Category.objects.all()
    return {
        'categories': categories
    }
    

def HomePage(request):
    return render(request, "home.htm")


def mainProduct(request):
    Products = Product.products.filter()
    count = Product.products.all().count()

    return render(request , "store/home.htm",context={
        "products": Products,
        "count": count
    })

 

def detailProduct(request , slug):
    item = get_object_or_404(Product, slug=slug , is_active=True)
    return render(request , "store/detail.htm" , context={
        'item': item
    })


def categoryList(request , slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.products.filter(category=category)

    return render(request , "store/category.htm" , context={
        'category': category,
        'products': products
    })
