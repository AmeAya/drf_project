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
    path('checkout', CheckOutApiView.as_view(), name='checkout_url'),
    path('api/my_history', HistoryApiView.as_view(), name='history_url'),
    path('api/paginated_products', ProductPaginatorApiView.as_view(), name='paginator_url'),
    path('api/product_search', ProductSearchApiView.as_view(), name='search_url'),
    path('api/product_price', ProductPriceApiView.as_view(), name='product_price_url'),

    path('swagger', SchemaView.with_ui()),
]

urlpatterns += [
    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'),
    path('cart/cart-detail/', cart_detail, name='cart_detail'),
]
