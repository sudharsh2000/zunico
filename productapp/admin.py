from django.contrib import admin

from productapp.models import Cart, CartItem, OrderItem, Wishlist, Address

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist)
admin.site.register(Address)