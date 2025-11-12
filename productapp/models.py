from django.db import models
from django.db.models import Sum

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
    @property
    def total_price(self):
        total_price=sum(item.total_price for item in self.items.all())
        return total_price
    @property
    def total_discount(self):
        total_discount=sum(item.discount for item in self.items.all())
        return total_discount
    @property
    def final_price(self):
        final_price=self.total_price-self.total_discount
        return final_price
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='items')
    Product = models.ForeignKey(Products, on_delete=models.CASCADE,related_name='products')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price
        super().save(*args, **kwargs)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

    house_name = models.CharField(max_length=150)
    street = models.CharField(max_length=150, blank=True, null=True)
    landmark = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100)

    pincode = models.CharField(max_length=10)

    address_type = models.CharField(
        max_length=20,
        choices=[('Home', 'Home'), ('Work', 'Work'), ('Other', 'Other')],
        default='Home'
    )

    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.city}"
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=50, choices=[
        ('COD', 'Cash on Delivery'),
        ('ONLINE', 'Online Payment'),
    ])
    payment_status = models.CharField(max_length=20, default='Pending')
    order_status = models.CharField(max_length=20, default='Processing')
    created_at = models.DateTimeField(auto_now_add=True)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True,related_name='Product')
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE,related_name='payment')
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.CharField(max_length=50, default='Pending')
    payment_mode = models.CharField(max_length=50, default='COD')
    created_at = models.DateTimeField(auto_now_add=True)
