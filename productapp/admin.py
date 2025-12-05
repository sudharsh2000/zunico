from django.contrib import admin

from productapp.models import Cart, CartItem, OrderItem, Wishlist

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist)