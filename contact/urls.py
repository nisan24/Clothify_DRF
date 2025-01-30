from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Contact_ViewSet

router = DefaultRouter()
router.register('', Contact_ViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
