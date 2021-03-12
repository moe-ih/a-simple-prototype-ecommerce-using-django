from django.http.response import JsonResponse
from store.models import Product
from django.shortcuts import render,get_object_or_404
from . import basket
from django.http import JsonResponse

# Create your views here.


def main_basket(request):
    baskets = basket.Basket(request)
    return render(request, "basket/basketMain.htm",
    context={
        'baskets': baskets
    })


def add_basket(request):
    basket_session = basket.Basket(request)
    if request.POST.get('action') == 'post':
        qty = int(request.POST.get("qty"))
        
        productId = int(request.POST.get("productid"))
        product = get_object_or_404(Product,id = productId)

        basket_session.add(product=product , qty=qty)
        
        basketqty = basket_session.__len__()
        response = JsonResponse({
            "qty": basketqty
        })

        return response


def delete_basket(request):
    basket_session = basket.Basket(request)
    if request.POST.get('action') == 'delete':
        productId = int(request.POST.get("productid"))
        basket_session.delete(product_id=productId)

        basketqty = basket_session.__len__()
        baskettotal = basket_session.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})

        return response

    
