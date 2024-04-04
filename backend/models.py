<<<<<<< Updated upstream
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.db import models

STATE_CHOICES = (
    ('basket', 'Статус корзины'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)

USER_TYPE_CHOICES = (
    ('shop', 'Магазин'),
    ('buyer', 'Покупатель'),

)
class UserManager(BaseUserManager):
    """
    Миксин для управления пользователями
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Стандартная модель пользователей
    """
    REQUIRED_FIELDS = []
    objects = UserManager()
    USERNAME_FIELD = 'email'
    email = models.EmailField(_('email address'), unique=True)
    company = models.CharField(verbose_name='Компания', max_length=40, blank=True)
    position = models.CharField(verbose_name='Должность', max_length=40, blank=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    type = models.CharField(verbose_name='Тип пользователя', choices=USER_TYPE_CHOICES, max_length=5, default='buyer')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Список пользователей"
        ordering = ('email',)
class Shop(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    url = models.URLField(verbose_name='Ссылка', blank=True, null=True)
    user = models.OneToOneField(User, blank=True, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ('-name',)

        def __str__(self):
            return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    shops = models.ManyToManyField(Shop, related_name='categories')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-name',)

        def __str__(self):
            return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('-name',)

        def __str__(self):
            return self.name


class ProductInfo(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    price_rrc = models.IntegerField()

    class Meta:
        verbose_name = 'Информация о товаре'
        verbose_name_plural = 'Информация о товарах'
        ordering = ('-name',)

        def __str__(self):
            return (f'{self.name} {self.shop} {self.product} '
                    f'{self.quantity} {self.price} {self.price_rrc}')


class Parameter(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'
        ordering = ('-name',)

        def __str__(self):
            return self.name


class ProductParameter(models.Model):
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    value = models.IntegerField()

    class Meta:
        verbose_name = 'Параметры продукта'
        verbose_name_plural = 'Параметры продуктов'


        def __str__(self):
            return f'{self.parameter} {self.product_info} {self.value}'


class Order(models.Model):
    user = models.CharField(max_length=100)
    dt = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-user',)

        def __str__(self):
            return f'{self.user} {self.dt} {self.status}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    quantity = models.IntegerField

    class Meta:
        verbose_name = 'Информация о заказе'
        verbose_name_plural = 'Информация о заказах'
        ordering = ('-order',)

        def __str__(self):
            return f'{self.order} {self.product} {self.shop} {self.quantity}'


class Contact(models.Model):
    type = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    value = models.IntegerField()

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ('-user',)
        def __str__(self):
            return self.user
=======
from django.contrib.auth.base_user import BaseUserManagerfrom django.contrib.auth.models import AbstractUserfrom django.contrib.auth.validators import UnicodeUsernameValidatorfrom django.utils.translation import gettext_lazy as _from django.db import modelsSTATE_CHOICES = (    ('basket', 'Статус корзины'),    ('new', 'Новый'),    ('confirmed', 'Подтвержден'),    ('assembled', 'Собран'),    ('sent', 'Отправлен'),    ('delivered', 'Доставлен'),    ('canceled', 'Отменен'),)USER_TYPE_CHOICES = (    ('shop', 'Магазин'),    ('buyer', 'Покупатель'),)class UserManager(BaseUserManager):    """    Миксин для управления пользователями    """    use_in_migrations = True    def _create_user(self, email, password, **extra_fields):        """        Create and save a user with the given username, email, and password.        """        if not email:            raise ValueError('The given email must be set')        email = self.normalize_email(email)        user = self.model(email=email, **extra_fields)        user.set_password(password)        user.save(using=self._db)        return user    def create_user(self, email, password=None, **extra_fields):        extra_fields.setdefault('is_staff', False)        extra_fields.setdefault('is_superuser', False)        return self._create_user(email, password, **extra_fields)    def create_superuser(self, email, password, **extra_fields):        extra_fields.setdefault('is_staff', True)        extra_fields.setdefault('is_superuser', True)        if extra_fields.get('is_staff') is not True:            raise ValueError('Superuser must have is_staff=True.')        if extra_fields.get('is_superuser') is not True:            raise ValueError('Superuser must have is_superuser=True.')        return self._create_user(email, password, **extra_fields)class User(AbstractUser):    """    Стандартная модель пользователей    """    REQUIRED_FIELDS = []    objects = UserManager()    USERNAME_FIELD = 'email'    email = models.EmailField(_('email address'), unique=True)    company = models.CharField(verbose_name='Компания', max_length=40, blank=True)    position = models.CharField(verbose_name='Должность', max_length=40, blank=True)    username_validator = UnicodeUsernameValidator()    username = models.CharField(        _('username'),        max_length=150,        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),        validators=[username_validator],        error_messages={            'unique': _("A user with that username already exists."),        },    )    is_active = models.BooleanField(        _('active'),        default=True,        help_text=_(            'Designates whether this user should be treated as active. '            'Unselect this instead of deleting accounts.'        ),    )    type = models.CharField(verbose_name='Тип пользователя', choices=USER_TYPE_CHOICES, max_length=5, default='buyer')    def __str__(self):        return f'{self.first_name} {self.last_name}'    class Meta:        verbose_name = 'Пользователь'        verbose_name_plural = "Список пользователей"        ordering = ('-email',)class Shop(models.Model):    name = models.CharField(max_length=100, verbose_name='Название')    url = models.URLField(verbose_name='Ссылка', blank=True, null=True)    user = models.OneToOneField(User, verbose_name='Пользователь',                                blank=True, null=True,                                on_delete=models.CASCADE)    state = models.BooleanField(verbose_name='Cтатус получения заказов', default=True)    class Meta:        verbose_name = 'Магазин'        verbose_name_plural = 'Магазины'        ordering = ('-name',)    def __str__(self):        return self.nameclass Category(models.Model):    name = models.CharField(max_length=100, verbose_name='Название')    shops = models.ManyToManyField(Shop, related_name='categories')    class Meta:        verbose_name = 'Категория'        verbose_name_plural = 'Категории'        ordering = ('-name',)    def __str__(self):        return self.nameclass Product(models.Model):    name = models.CharField(max_length=100, verbose_name='Название')    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')    class Meta:        verbose_name = 'Товар'        verbose_name_plural = 'Товары'        ordering = ('-name',)    def __str__(self):        return self.nameclass ProductInfo(models.Model):    name_model = models.CharField(max_length=100, verbose_name='Модель')    external_id = models.PositiveIntegerField(verbose_name='Внешний ID')    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Магазин')    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')    quantity = models.PositiveIntegerField(verbose_name='Количество')    price = models.PositiveIntegerField(verbose_name='Цена')    price_rrc = models.PositiveIntegerField(verbose_name='Рекомендуемая цена')    class Meta:        verbose_name = 'Информация о товаре'        verbose_name_plural = 'Информация о товарах'        constraints = [            models.UniqueConstraint(fields=['name_model', 'shop', 'product', 'quantity'], name='unique_product_info')        ]    def __str__(self):        return self.name_modelclass Parameter(models.Model):    name = models.CharField(max_length=100, verbose_name='Название')    class Meta:        verbose_name = 'Параметр'        verbose_name_plural = 'Параметры'    def __str__(self):        return self.nameclass ProductParameter(models.Model):    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, verbose_name='Параметр')    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, verbose_name='Информация о продукте')    value = models.CharField(max_length=100, verbose_name='Значение')    class Meta:        verbose_name = 'Параметры продукта'        verbose_name_plural = 'Параметры продуктов'    def __str__(self):        return f'{self.parameter} {self.product_info} {self.value}'class Contact(models.Model):    user = models.ForeignKey(User, verbose_name='Пользователь', max_length=100, on_delete=models.CASCADE)    city = models.CharField(max_length=100, verbose_name='Город')    street = models.CharField(max_length=100, verbose_name='Улица')    house = models.CharField(max_length=100, verbose_name='Дом', blank=True)    hull = models.CharField(max_length=100, verbose_name='Корпус', blank=True)    building = models.CharField(max_length=100, verbose_name='Строение', blank=True)    apartment = models.CharField(max_length=100, verbose_name='Квартира', blank=True)    phone = models.CharField(max_length=100, verbose_name='Телефон', blank=True)    class Meta:        verbose_name = 'Контакт'        verbose_name_plural = 'Информация о контактах'    def __str__(self):        return f'{self.city} {self.street} {self.house}'class Order(models.Model):    user = models.CharField(max_length=100, verbose_name='Пользователь')    dt = models.DateTimeField(auto_now_add=True)    status = models.CharField(verbose_name='Статус', choices=STATE_CHOICES, max_length=30)    contact = models.ForeignKey(Contact, verbose_name='Контакт', on_delete=models.CASCADE)    class Meta:        verbose_name = 'Заказ'        verbose_name_plural = 'Заказы'    def __str__(self):        return f'{self.user} {self.dt} {self.status}'class OrderItem(models.Model):    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Магазин')    quantity = models.PositiveIntegerField(verbose_name='Количество')    class Meta:        verbose_name = 'Информация о заказе'        verbose_name_plural = 'Информация о заказах'    def __str__(self):        return f'{self.order} {self.product} {self.shop} {self.quantity}'
>>>>>>> Stashed changes
