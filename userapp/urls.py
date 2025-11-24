"""
URL configuration for zunico_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from userapp import views

from zunico_django import settings

router = routers.DefaultRouter()
router.register('users',views.UsersViewSet, basename='users')
router.register(r'banners',views.BannersViewSet,basename='Banners')
router.register('signup',views.SignUpViewSet,basename='signup')



urlpatterns = [

path('',views.home,name='home'),
path('signin',views.LoginView.as_view(),name='signin'),
path('Refresh/',views.RefreshTokenview.as_view(),name='Refresh'),
path('logout/',views.LogoutView.as_view(),name='logout'),
path('create-admin',views.create_admin,name='create_admin'),
    path('api/', include(router.urls)),

]
