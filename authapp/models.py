from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    username_validator = ASCIIUsernameValidator()
    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        unique=True,
        validators=[username_validator],
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        validators=[
            RegexValidator(
                regex='^[А-Яа-яЁё]+$',
                message='Используйте только русские символы.'
            )
        ],
        null=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        validators=[
            RegexValidator(
                regex='^[А-Яа-яЁё]+$',
                message='Используйте только русские символы.'
            )
        ],
        null=True
    )
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=20, blank=True, null=True, unique=True)
    email = models.EmailField(verbose_name='Почта', unique=True)
    approval = models.CharField(verbose_name='Согласие на обработку персональных данных', max_length=50, blank=True, null=True, choices=[
        ('approval', 'Согласие на обработку персональных данных'),
    ])

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'users'
