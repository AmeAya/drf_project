from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import *


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'date_joined'
        ]


class PurchaseItemSerializer(ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = [
            'product', 'quantity', 'subtotal'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = ProductSerializer(instance.product, many=False).data
        representation['product'].pop('id')
        representation['product'].pop('description')
        representation['product']['price'] += '$'
        return representation


class PurchaseSerializer(ModelSerializer):
    class Meta:
        model = Purchase
        fields = [
            'items', 'total', 'created_at'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation - dict который дает на выходе сериалайзер
        # instance - сырой объект до прохода в сериалайзер

        # print(type(representation['created_at']))  # str
        # print(type(instance.created_at))  # datetime.datetime
        representation['created_at'] = instance.created_at.strftime("%d-%m-%Y %H:%M:%S")
        representation['items'] = PurchaseItemSerializer(instance.items.all(), many=True).data
        return representation


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email'
        ]
