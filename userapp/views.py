from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from userapp.Serializers import UserSerializer, BannersSerializer
from userapp.models import User, Banners

from django.contrib.auth import get_user_model
def home(request):
    return HttpResponse("Hello, world. You're at the polls page.")


def create_admin(req):
    User = get_user_model()
    username = "developer"
    email = "developer@example.com"
    password = "123"

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        return HttpResponse('Superuser created!')
    else:
         return HttpResponse("Superuser already exists!")
# Create your views here.
class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['username','email','id']
    search_fields = ['username','email']
class IsMyAAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser and request.user.is_authenticated
class BannersViewSet(viewsets.ModelViewSet):
    queryset = Banners.objects.all()
    serializer_class =BannersSerializer
class SignUpViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class LoginView(APIView):

    def post(self, request, *args, **kwargs):

        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('superuser')
        role=str(role).lower() in ['true','1','yes']
        print('username',username,role)
        print('password',password,role)
        user=authenticate(username=username, password=password)
        print('user',user,role)
        if user is None:
            return Response({'message': 'Invalid username or password.'}, status=401)
        if user.is_superuser!=role:
            return Response({'message': 'Invalid username or password.'}, status=401)
        refresh=RefreshToken.for_user(user)
        refresh['username']=user.username
        refresh['superuser']=user.is_superuser
        print('refresh-tok',refresh)
        response=Response({'access_token': str(refresh.access_token),'message': 'Successfully logged in.'})

        response.set_cookie(
            key='refresh', value=str(refresh),
            samesite='None',
            httponly=False,
            secure=True,

            max_age=7*24*60*60

        )

        return response
class RefreshTokenview(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')
        print('refresh-tok',request.COOKIES)
        print('refresh', refresh_token)

        if  refresh_token is None:
            return Response({'message': 'No refresh token'}, status=401)
        try:
                resfreshtok = RefreshToken(refresh_token)

                response = Response({'access_token': str(resfreshtok.access_token)})
                return response
        except TokenError as e:
                return Response({'message': 'Token error.'}, status=401)

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')
        token=RefreshToken(refresh_token)
        token.blacklist()
        response = Response({'data': 'Successfully logged out.'})
        response.delete_cookie(key='refresh')
        return response

