"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from app.views import *

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

SchemaView = get_schema_view(
    info=openapi.Info(
        title='DRF Project',
        default_version='1.0',
        description='This is pet project',
        terms_of_service='',
        contact=openapi.Contact(name='Dias Bolatov', url='', email='deobackstep@gmail.com'),
        license=openapi.License(name='License', url='')
    ),
    patterns=[
        path('api/products', ProductApiView.as_view(), name='products_api_url'),
        path('api/products/<int:pk>', ProductDetailApiView.as_view(), name='products_detail_api_url'),
    ],
    public=True,
    permission_classes=[AllowAny, ]
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products', ProductApiView.as_view(), name='products_api_url'),
    path('api/products/<int:pk>', ProductDetailApiView.as_view(), name='products_detail_api_url'),
    path('api/login', AuthApiView.as_view(), name='login_url'),
    path('api/profile', ProfileApiView.as_view(), name='profile_url'),
    path('api/language', LanguageApiView.as_view(), name='lang_url'),
    path('api/logout', LogOutApiView.as_view(), name='logout_url'),

    path('swagger', SchemaView.with_ui()),
]
