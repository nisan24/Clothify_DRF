from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
    path('api/shopping/', include('wishlist.urls')),
    path('api/contacts/', include('contact.urls')),
    path('api/', include('orders.urls')),
    path('api/payment/', include('payments.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
