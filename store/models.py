from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from django.conf import settings

class ProductManger(models.Manager):
    def get_queryset(self):
        return super(ProductManger,self).get_queryset().filter(is_active=True)


class Category(models.Model):
    name = models.CharField(max_length=255 , db_index=True)
    slug = models.SlugField(max_length=500 , unique=True)

    class Meta:
        verbose_name_plural = "categories"


    def get_absolute_url(self):
        return reverse("store:category_list", kwargs={"slug": self.slug})
    

    def __str__(self):
        return self.name



class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='product',
                                 on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name="product_creator",
                                   on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255 , default="Unknown")
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="images/", blank=True, default="images/NoImage.png")
    slug = models.SlugField(max_length=500)
    price = models.DecimalField(max_digits=6 , decimal_places=2)
    is_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    products = ProductManger()


    class Meta:
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.title
