from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.http import HttpResponse
from basket import basket
from .models import Order ,OrderItem

# Create your views here.


def add(request):
    print("Work")
    basket_session = basket.Basket(request)
    if request.POST.get('action') == 'post':
        user_id = request.user.id
        order_key = request.POST.get('order_key')
        baskettotal = basket_session.get_total_price()
        
        if Order.objects.filter(order_key=order_key).exists():
            pass
        
        else:
            order = Order.objects.create(user_id=user_id, full_name='name', address1='add1',
                                         address2='add2', total_paid=baskettotal, order_key=order_key)

            order_id = order.pk

            for item in basket_session:
                OrderItem.objects.create(
                    order_id=order_id, product=item['product'], price=item['price'],
                    qty=item['qty'])

        response = JsonResponse({'success': 'success'})
        return response


def payment_confirmation(secret):
    Order.objects.filter(order_key=secret).update(billing_status = True)
    
