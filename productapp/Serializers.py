from django.db.models.aggregates import Sum
from rest_framework import serializers

from productapp.models import Products, Productcategory, productimage, Cart, CartItem, Address


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = productimage
        fields = '__all__'
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True,read_only=True)
    class Meta:
        model = Products
        fields = ['id','name','category','price','description','cost_price','discount','stock', 'main_image', 'images']

    def create(self, validated_data):
        request = self.context.get('request')  # get request context
        images = request.FILES.getlist('images')  # get all uploaded images

        product = Products.objects.create(**validated_data)

        for img in images:
            productimage.objects.create(name=product, image=img)

        return product
class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Productcategory
        fields = '__all__'
class CartItemSerializer(serializers.ModelSerializer):
    Product = ProductSerializer(read_only=True)
    Product_id=serializers.PrimaryKeyRelatedField(queryset=Products.objects.all(), write_only=True,source='Product')


    class Meta:
        model = CartItem
        fields = ['id','Product','Product_id', 'quantity','price','total_price','discount']
        extra_kwargs = {
            'cart': {'read_only': True}
        }
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)


    class Meta:
        model = Cart
        fields = ['id','items','total_price','user','total_discount','final_price']
    def create(self, validated_data):
        items = validated_data.pop('items')
        user=validated_data.get('user')
        cart,created = Cart.objects.get_or_create(user=user)

        for item in items:



            Product=item['Product']
            print(Product.id)

            quantity=item.get('quantity')
            price=item.get('price')
            total_price=item.get('total_price')
            products=Products.objects.get(id=Product.id)
            olditem=CartItem.objects.filter(cart=cart, Product=Product).first()
            if olditem:

                olditem.quantity +=quantity
                olditem.total_price=olditem.price* olditem.quantity
                olditem.discount=(products.discount*100)/olditem.total_price
                olditem.save()
            else:

                CartItem.objects.create(cart=cart, **item)
                Cart.save()
        return cart


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'