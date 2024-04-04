from django.urls import path

from backend.views import PartnerUpdate, RegisterAccount, LoginAccount, ProductInfoView, CategoryView, ShopView, \
    OrderView, BasketView, ContactView, OrdersView, BasketsView, AccountDetails

app_name = 'backend'

urlpatterns = [
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    path('user/register', RegisterAccount.as_view(), name='user-register'),
    path('user/login', LoginAccount.as_view(), name='user-login'),
    path('user/contact/<int:pk>', ContactView.as_view(), name='contact'),
    path('user/account', AccountDetails.as_view(), name='account'),
    path('categories', CategoryView.as_view(), name='categories'),
    path('products', ProductInfoView.as_view(), name='products'),
    path('shops', ShopView.as_view(), name='shops'),
    path('order/<int:pk>', OrderView.as_view(), name='order'),
    path('order', OrdersView.as_view(), name='orders'),
    path('basket/<int:pk>', BasketView.as_view(), name='basket'),
    path('basket', BasketsView.as_view(), name='baskets')
]
