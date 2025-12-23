import hashlib
import hmac

import razorpay
from django.db.models import Max
from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from zunico_django import settings

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
from productapp.Serializers import ProductSerializer, ProductCategorySerializer, CartItemSerializer, CartSerializer, \
    AddressSerializer, OrderSerializer, OrderItemsSerializer, WishlistSerializer
from productapp.models import Products, Productcategory, productimage, CartItem, Cart, Address, Order, OrderItem, \
    Payment, Wishlist

class ProductPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 10
# Create your views here.
class products(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_fields = ['id', 'name','category','slug','price','description']
    pagination_class = ProductPagination
    search_fields = ['name','description','price','category__name']
    ordering_fields = ['name','price','updated_at']
    ordering = ['-updated_at']
class productcategories(viewsets.ModelViewSet):
    queryset = Productcategory.objects.all()
    serializer_class = ProductCategorySerializer
class ProductImages(viewsets.ModelViewSet):
    queryset = productimage.objects.all()
class CartViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'user']
    ordering_fields = ['user', 'latest_item_added']
    ordering = ['-latest_item_added']

    def get_queryset(self):
        return (
            Cart.objects
            .annotate(latest_item_added=Max('items__updated_at'))
            .distinct()
        )
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        user_id=request.GET.get ('user')
        print(user_id)
        if user_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Cart.objects.filter(user=user_id).delete()
        return Response(status=status.HTTP_200_OK)


class CartitemsViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
class AddressViewset(viewsets.ModelViewSet):
   
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'user']
class OrderItemViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'Product_id', 'quantity']

class OrderViewset(viewsets.ModelViewSet):


    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'user','order_status']


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_items = serializer.validated_data.pop('order_items')
        payment_data = serializer.validated_data.pop('payment')

        # Create the order in database
        order = Order.objects.create(**serializer.validated_data)

        # Create order items
        for item in order_items:
            OrderItem.objects.create(order=order, **item)

        # Create Payment object
        payment = Payment.objects.create(order=order, **payment_data)

        # If ONLINE payment -> create Razorpay order
        if order.payment_method == 'ONLINE':
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            razorpay_order = client.order.create({
                "amount": int(order.total_amount * 100),  # in paise
                "currency": "INR",
                "payment_capture": "1"
            })
            payment.razorpay_order_id = razorpay_order['id']
            payment.payment_mode = 'Razorpay'
            payment.save()

            return Response({
                "order_id": order.id,
                "razorpay_order_id": razorpay_order['id'],
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "amount": order.total_amount,
                "currency": "INR",
            }, status=status.HTTP_201_CREATED)

        # If COD -> just return normal response
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class VerifyPayment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            client.utility.verify_payment_signature({
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })

            payment = Payment.objects.get(razorpay_order_id=data['razorpay_order_id'])
            payment.razorpay_payment_id = data['razorpay_payment_id']
            payment.razorpay_signature = data['razorpay_signature']
            payment.payment_status = "Paid"
            payment.save()

            order = payment.order
            order.payment_status = "Paid"
            order.order_status = "Processing"
            order.save()

            return Response({"status": "success"})
        except Exception as e:
            return Response({"status": "failed", "message": str(e)}, status=400)
class DeleteDraftOrder(APIView):
    def delete(self, request):
        user = request.GET.get("user")
        status = request.GET.get("order_status")
        print(user,status)
        order= Order.objects.filter(user=user, order_status=status)
        if order is not None:
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(staus=status.HTTP_400_BAD_REQUEST)
class WishlistViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'user','Product_id',]