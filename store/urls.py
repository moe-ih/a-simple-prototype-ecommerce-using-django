from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("",views.mainProduct , name="mainproduct"),
    path("item/<slug:slug>/", views.detailProduct, name="product_detail"),
    path("category/<slug:slug>/", views.categoryList, name="category_list"),
]
