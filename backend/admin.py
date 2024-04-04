from django.contrib import admin

<<<<<<< Updated upstream
from .models import Shop
=======
from .models import Shop, ProductInfo, Category, Product, Parameter, ProductParameter, Order, OrderItem, Contact
>>>>>>> Stashed changes


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
<<<<<<< Updated upstream
    pass


=======
    list_display = ['name', 'user', 'state']
    list_filter = ['name', 'state']
    search_fields = ['name']
    list_per_page = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    list_per_page = 10


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['id', 'name']
    search_fields = ['id', 'name']
    list_per_page = 10


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ['name_model', 'quantity']
    list_filter = ['name_model', 'quantity']
    list_per_page = 10


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    list_per_page = 10


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    list_display = ['parameter']
    list_filter = ['parameter']
    search_fields = ['parameter']
    list_per_page = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'dt', 'status']
    list_filter = ['user', 'dt', 'status']
    # search_fields = ['status']
    list_per_page = 10


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'shop']
    list_filter = ['order', 'product', 'shop']
    list_per_page = 10


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']
    list_filter = ['user', 'phone']
    list_per_page = 10
>>>>>>> Stashed changes
