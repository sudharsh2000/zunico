from django.shortcuts import render
from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from productapp.Serializers import ProductSerializer, ProductCategorySerializer, CartItemSerializer, CartSerializer, \
    AddressSerializer
from productapp.models import Products, Productcategory, productimage, CartItem, Cart, Address


# Create your views here.
class products(viewsets.ModelViewSet):


    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'name','category','slug','price','description']



    search_fields = ['name','description','price','category__name']

class productcategories(viewsets.ModelViewSet):


    queryset = Productcategory.objects.all()
    serializer_class = ProductCategorySerializer
class ProductImages(viewsets.ModelViewSet):
    queryset = productimage.objects.all()
class CartViewset(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'user']
class CartitemsViewset(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
class AddressViewset(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'user']