from django.shortcuts import render
from rest_framework import generics, status
from . models import *
from rest_framework.viewsets import ModelViewSet
from . serializers import Product_Serializer, Review_Serializer, Category_Serializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from django.http import JsonResponse
from django.db.models import Q
# Create your views here.


class Product_View(ModelViewSet):
    queryset = Product_Model.objects.all()
    serializer_class = Product_Serializer

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = Q()

        # Category Filter -- Multiple Categories 
        categories = self.request.query_params.getlist("category", [])

        if categories:
            category_filter = Q()
            for cat in categories:
                category_filter |= Q(category__slug= cat)  
                category_filter |= Q(category__slug__icontains= cat)
                
                split_categories = cat.split("-")
                for split_cat in split_categories:
                    category_filter |= Q(category__slug__icontains= split_cat)
            
            filters &= category_filter


        # Brand Filter
        brand_name = self.request.query_params.get("brand", "")
        if brand_name:
            filters &= Q(brand__name__icontains= brand_name.lower())
            

        # Size Filter
        size = self.request.query_params.get("size", "")
        if size:
            filters &= Q(size= size.upper())


        # Color Filter
        color = self.request.query_params.get("color", "")
        if color:
            filters &= Q(color__icontains= color)
            

        # Price Range Filter
        min_price = self.request.query_params.get("min_price", "")
        max_price = self.request.query_params.get("max_price", "")

        if min_price and max_price:
            try:
                min_price = float(min_price)
                max_price = float(max_price)
                filters &= Q(price__gte= min_price, price__lte= max_price)
            except ValueError:
                pass
        elif min_price:
            try:
                min_price = float(min_price)
                filters &= Q(price__gte= min_price)
            except ValueError:
                pass
        elif max_price:
            try:
                max_price = float(max_price)
                filters &= Q(price__lte= max_price)
            except ValueError:
                pass
            

        # Search Filter
        search = self.request.query_params.get("search", "")
        if search:
            filters &= Q(name__icontains= search) | Q(description__icontains= search) | Q(brand__name__icontains= search)


        # Gender Filter  
        gender = self.request.query_params.get("categorys", None)
        if gender:
            # gender = gender.lower()
            filters &= Q(gender__iexact= gender.lower())


        # Sorting Filter
        sort_option = self.request.query_params.get("sort", "")
        if sort_option:
            if sort_option == "price-low":
                queryset = queryset.order_by("price")
            elif sort_option == "price-high":
                queryset = queryset.order_by("-price")
            elif sort_option == "latest":
                queryset = queryset.order_by("-create_time")

        return queryset.filter(filters)

# //=====================

# class Product_View(ModelViewSet):
#     queryset = Product_Model.objects.all()
#     serializer_class = Product_Serializer
    
#     def get_queryset(self):
#         queryset = super().get_queryset()
        
#         # Filter -------> brand name
#         search = self.request.query_params.get("search", '')
#         if search:
#             queryset = queryset.filter(name__icontains= search)
        
        
#         # Filter -------> brand name
#         brand_name = self.request.query_params.get("brand", '')
#         if brand_name:
#             queryset = queryset.filter(brand__name__icontains= brand_name)
        
        
#         # Filter -------> size
#         size = self.request.query_params.get("size", '')
#         if size:
#             queryset = queryset.filter(size= size)
        
        
#         # Filter --------> color
#         color = self.request.query_params.get("color", '')
#         if color:
#             queryset = queryset.filter(color__icontains= color)
        
        
#         # Filter ---------> category
#         category = self.request.query_params.get("category", '')
#         if category:
#             queryset = queryset.filter(category__name__icontains= category)
        
#         # Filter ---------> gender
#         gender = self.request.query_params.get("gender", '')
#         if gender:
#             queryset = queryset.filter(gender= gender)
        
#         return queryset



class Categories_View(ModelViewSet):
    queryset = Category_Model.objects.all()
    serializer_class = Category_Serializer
    
    

class Review_View(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, product_id, *args, **kwargs):
        reviews = Review_Model.objects.filter(product_id= product_id)
        serializer = Review_Serializer(reviews, many= True)
        return Response(serializer.data)

    def post(self, request, product_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required!"}, status= status.HTTP_401_UNAUTHORIZED)

        product = get_object_or_404(Product_Model, id= product_id)

        if Review_Model.objects.filter(user= request.user, product= product).exists():
            return Response({"detail": "You have already reviewed this product!"}, status= status.HTTP_400_BAD_REQUEST)

        data = {
            "user": request.user.id,
            "product": product.id,
            "rating": request.data.get("rating"),
            "comment": request.data.get("comment"),
        }

        serializer = Review_Serializer(data= data)

        if serializer.is_valid():
            serializer.save(user= request.user, product= product)
            return Response({"message": "Review added successfully!", "data": serializer.data}, status= status.HTTP_201_CREATED)

        return Response({"error": serializer.errors}, status= status.HTTP_400_BAD_REQUEST)

