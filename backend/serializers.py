from rest_framework import serializers

<<<<<<< Updated upstream
from models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, OrderItem, Contact
=======
from backend.models import (Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, OrderItem,
                            Contact,
                            User)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'company', 'position', 'type']
        read_only_fields = ['id']
>>>>>>> Stashed changes


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
<<<<<<< Updated upstream
        fields = '__all__'
=======
        fields = ['id', 'name', ]
        read_only = ['id',]
>>>>>>> Stashed changes


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
<<<<<<< Updated upstream
        fields = '__all__'
=======
        fields = ['id', 'name', 'shops', ]
>>>>>>> Stashed changes


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
<<<<<<< Updated upstream
        fields = '__all__'


class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = ['name', 'shop', 'product', 'price']
=======
        fields = ['id', 'name']


class ProductInfoSerializer(serializers.ModelSerializer):
    shop = ShopSerializer(read_only=True)

    class Meta:
        model = ProductInfo
        fields = ['id', 'name_model', 'external_id', 'shop', 'product', 'quantity', 'price', 'price_rrc']
        read_only = ['id']
>>>>>>> Stashed changes


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['name']


class ProductParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductParameter
<<<<<<< Updated upstream
        fields = '__all__'
=======
        fields = ['id', 'product_id', 'parameter_id', 'value']
>>>>>>> Stashed changes


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
<<<<<<< Updated upstream
        fields = '__all__'
=======
        fields = ['id', 'user', 'dt', 'status', 'contact']
>>>>>>> Stashed changes


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
<<<<<<< Updated upstream
        fields = '__all__'
=======
        fields = ['id', 'order_id', 'product_id', 'shop_id', 'quantity']
>>>>>>> Stashed changes


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
<<<<<<< Updated upstream
        fields = '__all__'
=======
        fields = ['id', 'user_id', 'city', 'street', 'house', 'hull', 'building', 'apartment', 'phone']
>>>>>>> Stashed changes
