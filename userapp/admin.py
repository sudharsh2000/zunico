from django.contrib import admin

from productapp.models import Products, productimage, Productcategory, Payment, OrderItem, Order
from .models import User, Banners

# Register your models here.
admin.site.register(User)
admin.site.register(Banners)
admin.site.register(Products)
admin.site.register(Productcategory)
admin.site.register(productimage)
admin.site.register(Payment)
admin.site.register(OrderItem)
admin.site.register(Order)