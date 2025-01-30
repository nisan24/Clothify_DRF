from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("wishlist/add/", Add_Wishlist_View.as_view(), name= "wishlist-add"),
    path("wishlist/", Wishlist_ListView.as_view(), name= "wishlist-list"),
    path("wishlist/check/<int:product_id>/", Wishlist_Check_View.as_view(), name="wishlist-check"),
    path("wishlist/remove/<int:product_id>/", Wishlist_Remove_View.as_view(), name="wishlist-remove"),

    path("cart/add/", AddToCart.as_view(), name= "cart-add"),
    path("cart/", Cart_ListView.as_view(), name= "cart-list"),
    path("cart/remove/<int:product_id>/", CartItem_Remove_view.as_view(), name= "removeItem-cart"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
