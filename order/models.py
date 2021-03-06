from django.db import models
from django.db.models.deletion import CASCADE

from store.models import Product
from django.conf import settings


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=CASCADE, related_name="order_user")

    full_name = models.CharField(max_length=50)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=5, decimal_places=2)
    order_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(default=False)


    class Meta:
        ordering = ('-created',)

    
    def __str__(self):
        return str(self.created)


class OrderItem(models.Model):
    order = models.ForeignKey(Order , on_delete=CASCADE , related_name="item")
    product = models.ForeignKey(Product , on_delete=CASCADE , related_name="order_item")
    price = models.DecimalField(max_digits=6 , decimal_places=3)
    qty = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
