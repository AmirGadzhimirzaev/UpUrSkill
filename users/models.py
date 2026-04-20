from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('email обязательное поле')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have if_superuser=True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True,
        verbose_name='email'
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='номер телефона'
    )
    city = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name='город'
    )
    avatar = models.ImageField(
        upload_to='users/avatar/',
        blank=True,
        null=True,
        verbose_name='аватарка'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email


class Payments(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = 'наличные'
        CARD = 'перевод на карту'

    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='id сессии',
        help_text='укажите id'
    )
    link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='ссылка на платеж',
        help_text='укажите ссылку на оплату'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Пользователь',
        related_name='payer'
    )
    product_id = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='id продукта'
    )
    price_id = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='id цены'
    )
    currency = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='валюта'
    )
    date = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
        verbose_name='дата создания продукта'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='курс на оплату',
        related_name='paid_course'
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='урок на оплату',
        related_name='paid_lesson'
    )
    payment_amount = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='сумма оплаты'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        blank=True,
        null=True,
        verbose_name='способ платежа: наличные или перевод на счет'
    )
    payment_status = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='статус оплаты'
    )

    def __str__(self):
        return f'{self.course.name} - {self.payment_amount} {self.currency}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'


class Subscription(models.Model):
    sub_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Подписка пользователя',
    )
    sub_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Курс по подписке'
    )

    def __str__(self):
        return f'{self.sub_user}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
