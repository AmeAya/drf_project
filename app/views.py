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

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # save() -> Сохранить объект их сериалайзера в БД
            # return Response(data={'msg': 'Product Created successfully!'}, status=status.HTTP_201_CREATED)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailApiView(APIView):
    permission_classes = []

    def get(self, request, pk):
        from django.shortcuts import get_object_or_404
        product = get_object_or_404(Product, id=pk)
        data = {
            'product': ProductSerializer(product, many=False).data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        from django.shortcuts import get_object_or_404
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        # partial=True - Означает что обновляются не все поля, а только часть из них
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        from django.shortcuts import get_object_or_404
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return Response(data={'msg': 'Product deleted!'}, status=status.HTTP_204_NO_CONTENT)


# Создать новую модель(Минимум 3 поля)
# Создать две вью для данной модели:
# 1) APIView - get, post
# 2) DetailAPIView - get, patch, delete
# Создать сериалайзер
