from django.db import models
from django.utils.text import slugify

from userapp.models import User
from zunico_django import settings


# Create your models here.
class Productcategory(models.Model):
        name = models.CharField(max_length=100)
        slug = models.SlugField(max_length=100, unique=True,blank=True,null=True)
        image=models.ImageField(upload_to='categories/', null=True, blank=True)
        def __str__(self):
            return self.name
        def save(self, *args, **kwargs):
            if not self.slug:
                self.slug=slugify(self.name)
            return super().save(*args, **kwargs)

class Products(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Productcategory, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True,null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount=models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    main_image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    def __str__(self):
        return self.name
class productimage(models.Model):
    name = models.ForeignKey(Products, on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='products/', null=True, blank=True)
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.user.username
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='items')
    Product = models.ForeignKey(productimage, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price
        super().save(*args, **kwargs)
