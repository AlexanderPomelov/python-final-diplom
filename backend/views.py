<<<<<<< Updated upstream
from django.shortcuts import render

=======
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from requests import get

from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from yaml import load as load_yaml, Loader

from backend.models import Shop, Category, ProductInfo, Product, Parameter, ProductParameter, Order, Contact, User
from backend.serializers import UserSerializer, CategorySerializer, ShopSerializer, ProductInfoSerializer, \
    OrderSerializer, ContactSerializer


class RegisterAccount(APIView):
    """
    Для регистрации покупателей
        """

    # Регистрация методом POST

    def post(self, request, *args, **kwargs):
        """
            Process a POST request and create a new user.

            Args:
                request (Request): The Django request object.

            Returns:
                JsonResponse: The response indicating the status of the operation and any errors.
            """
        # проверяем обязательные аргументы
        if {'first_name', 'last_name', 'email', 'password', 'company', 'position'}.issubset(request.data):

            # проверяем пароль на сложность
            sad = 'asd'
            try:
                validate_password(request.data['password'])
            except Exception as password_error:
                error_array = []
                # noinspection PyTypeChecker
                for item in password_error:
                    error_array.append(item)
                return JsonResponse({'Status': False, 'Errors': {'password': error_array}})
            else:
                # проверяем данные для уникальности имени пользователя

                user_serializer = UserSerializer(data=request.data)
                if user_serializer.is_valid():
                    # сохраняем пользователя
                    user = user_serializer.save()
                    user.set_password(request.data['password'])
                    user.save()
                    return JsonResponse({'Status': True})
                else:
                    return JsonResponse({'Status': False, 'Errors': user_serializer.errors})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class LoginAccount(APIView):
    """
    Для авторизации покупателей
        """

    def post(self, request):
        if {'email', 'password'}.issubset(request.data):
            user = authenticate(request, username=request.data['email'], password=request.data['password'])
            if user is not None:
                if user.is_active:
                    token, _ = Token.objects.get_or_create(user=user)
                    return JsonResponse({'Status': True, 'Text': f'Авторизация прошла успешно, Ваш токен: {token.key}'})
            return JsonResponse({'Status': False, 'Errors': 'Не правильно введен email или пароль'})

        return JsonResponse({'Status': False, 'Errors': 'Проверьте вводимые данные, не введены все аргументы'})


class AccountDetails(ListAPIView):
    """
    Получение информации об аккаунте
        """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Проверка аутентификации пользователя
    permission_classes = [IsAuthenticated]


class PartnerUpdate(APIView):
    """
    A class for updating partner information.

    Methods:
    - post: Update the partner information.

        """

    def post(self, request, *args, **kwargs):
        """
                Update the partner price list information.

                Args:
                - request (Request): The Django request object.

                Returns:
                - JsonResponse: The response indicating the status of the operation and any errors.
                """
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.type != 'shop':
            return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        url = request.data.get('url')
        if url:
            validate_url = URLValidator()
            try:
                validate_url(url)
            except ValidationError as e:
                return JsonResponse({'Status': False, 'Error': str(e)})
            else:
                stream = get(url).content

                data = load_yaml(stream, Loader=Loader)

                shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id)
                for category in data['categories']:
                    category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
                    category_object.shops.add(shop.id)
                    category_object.save()
                ProductInfo.objects.filter(shop_id=shop.id).delete()
                for item in data['goods']:
                    product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

                    product_info = ProductInfo.objects.create(product_id=product.id,
                                                              external_id=item['id'],
                                                              name_model=item['model'],
                                                              price=item['price'],
                                                              price_rrc=item['price_rrc'],
                                                              quantity=item['quantity'],
                                                              shop_id=shop.id)
                    for name, value in item['parameters'].items():
                        parameter_object, _ = Parameter.objects.get_or_create(name=name)
                        ProductParameter.objects.create(product_info_id=product_info.id,
                                                        parameter_id=parameter_object.id,
                                                        value=value)

                return JsonResponse({'Status': True})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class CategoryView(ListAPIView):
    """
    Получение списка категорий
        """

    # Получение всего списка категорий
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ShopView(ListAPIView):
    """
    Получение списка магазинов
        """

    # Получение всего списка магазинов
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class ProductInfoView(ListAPIView):
    """
    Получение списка товаров
        """

    # Получение всего списка товаров
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer

    # Подключаем фильтрацию и поиск для товаров
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['name_model', 'shop', 'product', 'quantity', 'price']
    search_fields = ['name_model']
    ordering_fileds = ['id', 'shop', 'quantity', 'price', 'price_rrc']


class BasketView(RetrieveUpdateDestroyAPIView):
    """
    Для получения информации о заказе в корзине
        """

    # Получение конкретного заказа в коризне
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # Проверка аутентификации пользователя
    permission_classes = [IsAuthenticated]


class BasketsView(ListCreateAPIView):
    """
    Для получения информации о всех заказах в корзине
        """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # Проверка аутентификации пользователя
    permission_classes = [IsAuthenticated]
    # Подключаем фильтрацию и поиск для товаров
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'contact']
    ordering_fields = ['id', 'user', 'dt', 'status']
    search_fields = ['user']


class OrderView(RetrieveUpdateAPIView):
    """
    Для получения информации о конкретном заказе
        """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # проверка аутентификации пользователя
    permission_classes = [IsAuthenticated]


class OrdersView(ListCreateAPIView):
    """
    Для получения информации о всех заказах
        """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # Проверка аутентификации пользователя
    permission_classes = [IsAuthenticated]
    # Подключаем фильтрацию и поиск для товаров
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['contact']
    ordering_fields = ['id', 'user']
    search_fields = ['id']


class ContactView(RetrieveUpdateDestroyAPIView):
    """
    Для получения информации и изменении данных контакта
        """

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    # Проверка аутентификации пользователя
    permission_classes = [IsAuthenticated]
>>>>>>> Stashed changes
