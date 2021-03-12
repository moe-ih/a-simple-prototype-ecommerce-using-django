from store.models import Product
from decimal import *
from django.conf import settings
class Basket(object):
    
    def __init__(self,request):
        self.session = request.session
        basket_session = self.session.get("basket_")

        if 'basket_' not in request.session:
            basket_session = self.session['basket_'] = {}
        self.current_basket_session = basket_session


    def add(self , product,qty):
        product_id = product.id

        if product_id not in self.current_basket_session:
            self.current_basket_session[product_id] = {'price': str(product.price)
            ,"qty": int(qty)}


        self.save()

    
    def __len__(self):
        return sum(item['qty'] for item in self.current_basket_session.values())


    def __iter__(self):

        products_id = self.current_basket_session.keys()
        proudcts = Product.products.filter(id__in=products_id)
        basket = self.current_basket_session.copy()

        for product in proudcts:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price']  * item['qty']
            yield(item)


    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.current_basket_session.values())
        
    def save(self):
        self.session.modified = True
    
    
    def delete(self , product_id):
        product = str(product_id)
        print(product)
        if product in self.current_basket_session:
            del self.current_basket_session[product]
            self.save()

    def clear(self):
        del self.session["basket_"]
        self.save()

    
