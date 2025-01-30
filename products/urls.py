from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register('list', Product_View)
router.register('category', Categories_View)


urlpatterns = [
    path("", include(router.urls)),
    # path("list/", Product_View.as_view(), name="product-list"),
    path('reviews/<int:product_id>/', Review_View.as_view(), name='product-reviews'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

