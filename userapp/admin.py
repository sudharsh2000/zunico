from django.contrib import admin

from productapp.models import Products,productimage,Productcategory
from .models import User, Banners

# Register your models here.
admin.site.register(User)
admin.site.register(Banners)
admin.site.register(Products)
admin.site.register(Productcategory)
admin.site.register(productimage)