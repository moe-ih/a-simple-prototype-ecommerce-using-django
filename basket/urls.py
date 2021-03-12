from django.urls import path
from . import views

app_name = "basket"

urlpatterns = [
    path("", views.main_basket , name="main_basket"),
    path("add_basket/", views.add_basket,name="basket_add"),
    path('delete_basket/', views.delete_basket, name='delete_basket'),
]
