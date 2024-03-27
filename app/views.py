from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status


class ProductApiView(APIView):
    permission_classes = []

    def get(self, request):
        products = Product.objects.all()
        data = {
            'products': ProductSerializer(products, many=True).data
        }
        # many = True ставится если нужно сериализовать несколько объектов
        return Response(data=data, status=status.HTTP_200_OK)
