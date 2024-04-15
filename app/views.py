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

    def get(self, request):  # READ USER
        if request.user.is_authenticated:
            data = UserSerializer(request.user, many=False).data
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(data={'msg': 'You must login!'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        from django.db.utils import IntegrityError
        username = request.data.get('username')
        fn = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')
        email = request.data.get('email')
        try:
            user = User.objects.create_user(username=username, first_name=fn, last_name=last_name, password=password,
                                            email=email)
            data = UserSerializer(user, many=False).data
            return Response(data=data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(data={'msg': 'This username is already taken'}, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request):
        if request.user.is_authenticated:
            serializer = UserUpdateSerializer(request.user, partial=True, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'msg': 'You must login!'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        if request.user.is_authenticated:
            request.user.is_active = False
            request.user.save()
            return Response(data={'msg': 'Your account successfully deactivated!'}, status=status.HTTP_400_BAD_REQUEST)
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

from cart.cart import Cart
from django.http import JsonResponse


def cart_add(request, id):
    if not request.user.is_authenticated:
        return JsonResponse(data={'msg': 'You have to log in!'}, status=status.HTTP_403_FORBIDDEN)
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return JsonResponse(data={'msg': 'Item added!'}, status=status.HTTP_200_OK)


def item_clear(request, id):
    if not request.user.is_authenticated:
        return JsonResponse(data={'msg': 'You have to log in!'}, status=status.HTTP_403_FORBIDDEN)
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return JsonResponse(data={'msg': 'Item deleted!'}, status=status.HTTP_200_OK)


def item_increment(request, id):
    if not request.user.is_authenticated:
        return JsonResponse(data={'msg': 'You have to log in!'}, status=status.HTTP_403_FORBIDDEN)
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return JsonResponse(data={'msg': 'Item quantity incremented!'}, status=status.HTTP_200_OK)


def item_decrement(request, id):
    if not request.user.is_authenticated:
        return JsonResponse(data={'msg': 'You have to log in!'}, status=status.HTTP_403_FORBIDDEN)
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return JsonResponse(data={'msg': 'Item quantity decremented!'}, status=status.HTTP_200_OK)


def cart_clear(request):
    if not request.user.is_authenticated:
        return JsonResponse(data={'msg': 'You have to log in!'}, status=status.HTTP_403_FORBIDDEN)
    cart = Cart(request)
    cart.clear()
    return JsonResponse(data={'msg': 'Cart cleared!'}, status=status.HTTP_200_OK)


def cart_detail(request):
    if not request.user.is_authenticated:
        return JsonResponse(data={'msg': 'You have to log in!'}, status=status.HTTP_403_FORBIDDEN)
    cart = Cart(request)
    cart_items = []
    total = 0
    for key, value in cart.cart.items():
        subtotal = float(value.get('price')) * int(value.get('quantity'))
        value.update({'subtotal': subtotal})
        total += subtotal
        cart_items.append(value)

    data = {
        'items': cart_items,
        'total': total
    }
    return JsonResponse(data=data, status=status.HTTP_200_OK)


class CheckOutApiView(APIView):
    permission_classes = []

    def post(self, request):
        cart = Cart(request)
        total = 0

        if cart.cart:
            purchase = Purchase(total=0, customer=request.user)
            purchase.save()

            for key, value in cart.cart.items():
                subtotal = float(value.get('price')) * int(value.get('quantity'))
                total += subtotal

                product = Product.objects.get(id=value.get('product_id'))
                item = PurchaseItem(product=product, quantity=value.get('quantity'), subtotal=subtotal)
                item.save()

                purchase.items.add(item)
                purchase.save()

            purchase.total = total
            purchase.save()
            cart.clear()
            return Response(data={'msg': 'Check out!'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'msg': 'Cart empty!'}, status=status.HTTP_400_BAD_REQUEST)


from django.core.paginator import Paginator, EmptyPage


class HistoryApiView(APIView):
    permission_classes = []

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(data={'msg': 'You have to log in!'}, status=status.HTTP_400_BAD_REQUEST)
        purchases = Purchase.objects.filter(customer=request.user)
        paginator = Paginator(purchases, 2)
        page = request.GET.get('page')
        if page is None:
            page = 1
        try:
            paginated_purchases = paginator.page(page)
        except EmptyPage:
            paginated_purchases = []

        data = {
            "purchases": PurchaseSerializer(paginated_purchases, many=True).data,
            "pages": paginator.num_pages
        }
        return Response(data=data, status=status.HTTP_200_OK)
    # Добавить paginator для HistoryApiView(get) по 2 покупки на странице.


class ProductPaginatorApiView(APIView):
    permission_classes = []

    def get(self, request):
        products = Product.objects.all()
        paginator = Paginator(products, 2)
        page = request.GET.get('page')
        if page is None:
            page = 1
        try:
            paginated_products = paginator.page(page)
        except EmptyPage:
            paginated_products = paginator.page(1)
        data = {
            "products": ProductSerializer(paginated_products, many=True).data,
            "pages": paginator.num_pages
        }
        return Response(data=data, status=status.HTTP_200_OK)


# class testApiView(APIView):  # ОДНОРАЗОВАЯ АПИ ЧТОБЫ ВЕРНУТЬ ПАРОЛЬ АДМИНУ. УДАЛИТЬ ПОСЛЕ ИСПОЛЬЗОВАНИЯ
#
#     def get(self, request):
#         user = User.objects.get(username='admin')
#         user.set_password('qwerty')
#         user.save()
#         return Response()


class ProductSearchApiView(APIView):
    permission_classes = []

    def get(self, request):
        from django.db.models import Q
        q = request.GET.get('q')
        if q is None:
            return Response(data=[], status=status.HTTP_200_OK)
        products = Product.objects.filter(~Q(name__contains=q) | ~Q(description__contains=q))
        # | - Or - ИЛИ
        # & - And - И
        # ~ - Negate - НЕ

        # products = Product.objects.filter(name__contains=q)
        # new = Product.objects.filter(description__contains=q)
        # products = products.union(new)
        # __contains - Ищет указанную часть в текст этого поля учитывая регистр
        # __icontains - То же самое что и contains, но игнорирует регистр

        data = ProductSerializer(products, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)


class ProductPriceApiView(APIView):
    permission_classes = []

    def get(self, request):
        from django.db.models import Q
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        if price_min is None or price_max is None:
            products = Product.objects.all()
        else:
            products = Product.objects.filter(Q(price__gte=price_min) & Q(price__lte=price_max))

            # products_min = Product.objects.filter(price__lte=price_max)
            # products_max = Product.objects.filter(price__gte=price_min)
            # products = products_min.union(products_max)

        data = ProductSerializer(products, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
