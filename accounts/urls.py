from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.UserRegistrationAPIView.as_view(), name= 'register'),
    path('login/', views.UserLoginApiView.as_view(), name= 'user_login'),
    path('logout/', views.UserLogoutApiView.as_view(), name= 'logout'),
    path('verify/<str:uid64>/<str:token>/', views.activate, name= 'activate'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),

]

