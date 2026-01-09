"""
URL configuration for zunico_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from productapp.Serializers import WishlistSerializer
from productapp.views import productimage, products, productcategories, CartViewset, CartitemsViewset, AddressViewset, \
    OrderViewset, OrderItemViewset, VerifyPayment, DeleteDraftOrder,WishlistViewset,NotificationViewSet

from zunico_django import settings

router = routers.DefaultRouter()
router.register('categories',productcategories, basename='productcategory')
router.register('products',products ,basename='products')
router.register('cart',CartViewset ,basename='cart')
router.register('cartitem',CartitemsViewset ,basename='cartitem')
router.register('addAdress',AddressViewset ,basename='addAdress')
router.register('orders',OrderViewset ,basename='orders')
router.register('orderitems',OrderItemViewset ,basename='orderitems')
router.register('wishlist',WishlistViewset ,basename='wishlist')
router.register('notification',NotificationViewSet ,basename='notification')
urlpatterns = [


    path('api/', include(router.urls)),
    path('api/payment/verify',VerifyPayment.as_view(),name='verify'),
    path('api/orders/delete-draft', DeleteDraftOrder.as_view(),name='delete_draft_order'),



]
