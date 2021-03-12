from django.urls import path
from .views import *

app_name = "payment"

urlpatterns = [

    path("", main , name="main"),
    path('orderplaced/', order_success, name="orderplaced"),
    path('webhook/', stripe_webhook)

]
