from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import parsers
from rest_framework.permissions import IsAuthenticated


class ProductApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        products = Product.objects.all()
        data = {
            'products': ProductSerializer(products, many=True).data
        }
        # many = True ставится если нужно сериализовать несколько объектов
        return Response(data=data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ProductSerializer,
        responses={
            201: 'Product is added to DB',
            400: 'Serializer error. For more info watch response'
        },
        security=[],
        operation_id='Create Product',
        operation_description='This API for creating new product into database',
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # save() -> Сохранить объект их сериалайзера в БД
            # return Response(data={'msg': 'Product Created successfully!'}, status=status.HTTP_201_CREATED)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailApiView(APIView):
    permission_classes = []
    parser_classes = [parsers.FormParser, parsers.JSONParser]

    def get(self, request, pk):
        from django.shortcuts import get_object_or_404
        product = get_object_or_404(Product, id=pk)
        data = {
            'product': ProductSerializer(product, many=False).data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='name', in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter(name='description', in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter(name='price', in_=openapi.IN_FORM, type=openapi.TYPE_NUMBER, required=False)
        ],
        responses={
            200: 'Product is updated',
            400: 'Serializer error. For more info watch response',
            404: 'Product not found'
        },
        operation_id='Update Product',
        operation_description='This API for updating existing product in database',
    )
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


class AuthApiView(APIView):
    permission_classes = []

    def post(self, request):
        from django.contrib.auth import authenticate, login

        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ProfileApiView(APIView):
    permission_classes = []

    def get(self, request):
        if request.user.is_authenticated:
            data = UserSerializer(request.user, many=False).data
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(data={'msg': 'You must login!'}, status=status.HTTP_401_UNAUTHORIZED)


class LanguageApiView(APIView):
    permission_classes = []

    def get(self, request):
        if 'selected_lang' not in request.session.keys():
            return Response(data={'msg': 'First select Lang!'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'Selected Language': request.session.get('selected_lang')}, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.is_authenticated:
            language = request.data.get('language')
            if language is not None:
                request.session.update({'selected_lang': language})
                return Response(data={'msg': 'Lang selected!'}, status=status.HTTP_200_OK)
            else:
                request.session.update({'selected_lang': 'english'})
                return Response(data={'msg': 'Lang selected!'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'msg': 'You must login!'}, status=status.HTTP_401_UNAUTHORIZED)


class LogOutApiView(APIView):
    permission_classes = []

    def post(self, request):
        from django.contrib.auth import logout

        if request.user.is_authenticated:
            logout(request)
            return Response(data={'msg': 'Logout successful!'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'msg': 'You must login!'}, status=status.HTTP_401_UNAUTHORIZED)
        # 1) Проверить авторизован ли пользователь
        # 2) Импортировать logout из django.contrib.auth
        # 3) Выполнить logout и вернуть response что logout прошел успешно
