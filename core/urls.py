from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from store import views

urlpatterns = [
    path("", views.HomePage, name="home"),
    path('admin/', admin.site.urls),
    path('product/', include("store.urls" , namespace="store")),
    path("basket/" , include("basket.urls",namespace="basket")),
    path("account/" , include("account.urls",namespace="account")),
    path("payment/", include("payment.urls", namespace="payment")),
    path("order/", include("order.urls", namespace="order")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    
