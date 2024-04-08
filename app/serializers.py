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
