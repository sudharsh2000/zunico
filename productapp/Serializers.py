from django.db.models.aggregates import Sum
from rest_framework import serializers

from productapp.models import Products, Productcategory, productimage, Cart, CartItem, Address, OrderItem, Payment, \
    Order


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
        fields = ['id','Product','Product_id', 'quantity','price','total_price','discount','added_at','updated_at']
        extra_kwargs = {
            'cart': {'read_only': True}
        }


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)


    class Meta:
        model = Cart
        fields = ['id','items','total_price','user','total_discount','final_price']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Order items descending by added_at
        data['items'] = sorted(data['items'], key=lambda i: i['added_at'], reverse=True)
        return data
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

    def get_items(self, obj):
        items = obj.items.all().order_by('-updated_at')
        return CartItemSerializer(items, many=True).data
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        extra_kwargs = {
            'order': {'read_only': True}
        }
class OrderItemsSerializer(serializers.ModelSerializer):
    Product = ProductSerializer(read_only=True)
    Product_id = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all(), write_only=True, source='Product')
    class Meta:
        model=OrderItem
        fields=['id','Product','quantity','price','total_price','Product_id','order']
        extra_kwargs = {
            "order": {"read_only": True}
        }
class OrderSerializer(serializers.ModelSerializer):
    order_items=OrderItemsSerializer(many=True)
    payment=PaymentSerializer()

    class Meta:
        model = Order
        fields = ['id','order_items','payment', 'total_amount','user','total_discount','payment_status','payment_method','order_status']
    def create(self, validated_data):
        order_items=validated_data.pop('order_items')
        payment=validated_data.pop('payment')
        order=Order.objects.create(**validated_data)
        print(payment)

        Payment.objects.create(**payment,order=order)
        for order_item in order_items:
            OrderItem.objects.create(order=order, **order_item)
        return order