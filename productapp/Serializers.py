from rest_framework import serializers

from productapp.models import Products, Productcategory, productimage, Cart, CartItem


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
    class Meta:
        model = CartItem
        fields = '__all__'
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id','user','items']
