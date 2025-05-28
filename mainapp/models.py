from django.db import models
from django.core.validators import RegexValidator

from authapp.models import User


class Category(models.Model):
    name = models.CharField(verbose_name='Категория', max_length=120)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Products(models.Model):
    category = models.ForeignKey(Category, verbose_name='Выберите категорию', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Название товара', max_length=120)
    image = models.ImageField(verbose_name='Изображение товара', upload_to='products/%Y/%m/%d')
    price = models.DecimalField(verbose_name='Цена', max_digits=15, decimal_places=2)
    desc = models.TextField(verbose_name='Описание')
    counts = models.IntegerField(verbose_name='Количество товара', default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Rubric(models.Model):
    rubric_name = models.CharField(verbose_name='Рубрика статьи', max_length=120)

    def __str__(self):
        return self.rubric_name

    class Meta:
        verbose_name = 'Рубрика статьи'
        verbose_name_plural = 'Рубрики статей'


class Article(models.Model):
    rubric = models.ForeignKey(Rubric, verbose_name='Выберите рубрику статьи', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок статьи', max_length=120)
    image = models.ImageField(verbose_name='Изображение статьи', upload_to='article/%Y/%m/%d')
    text = models.TextField(verbose_name='Текст статьи')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class ArticleLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_likes')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    liked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')
        verbose_name = 'Лайк статьи'
        verbose_name_plural = 'Лайки статей'


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    counts = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_basket_item')
        ]


class Favorites(models.Model):
    product = models.ForeignKey(Products, verbose_name='Товар', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Отзыв')
    rating = models.IntegerField(verbose_name='Оценка', choices=[
        (1, '1 звезда'),
        (2, '2 звезды'),
        (3, '3 звезды'),
        (4, '4 звезды'),
        (5, '5 звезд'),
    ])
    is_active = models.CharField(verbose_name='Статус отзыва', max_length=50, choices=[
        ('published', 'Опубликован'),
        ('cancelled', 'Отменен'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Order(models.Model):
    order_status = models.CharField(
        verbose_name='Статус доставки',
        max_length=50,
        choices=[
            ('decorated', 'Оформлен'),
            ('delivery', 'В пути'),
            ('delivered', 'Доставлен'),
        ],
        default='decorated'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender_name = models.CharField(
        verbose_name='Имя отправителя',
        max_length=150,
        null=True
    )
    phone_number = models.CharField(verbose_name='Номер телефона отправителя', max_length=20, null=True)
    recipient_name = models.CharField(
        verbose_name='Имя получателя',
        max_length=150,
        null=True
    )
    recipient_phone = models.CharField(verbose_name='Номер телефона получателя', max_length=20, null=True)
    delivery_type = models.CharField(verbose_name='Тип доставки', max_length=50, choices=[
        ('pickup', 'Самовывоз'),
        ('courier', 'Доставка курьером'),
    ])

    address = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    time = models.TimeField()
    comment = models.CharField(max_length=255, blank=True)

    pay_type = models.CharField(verbose_name='Тип оплаты', max_length=50, choices=[
        ('cash', 'Наличными'),
        ('card', 'Картой при получении'),
        ('online', 'Оплатить онлайн'),
    ])
    card_number = models.CharField(max_length=255, blank=True)
    CVV = models.CharField(max_length=255, blank=True)

    bouquets = models.JSONField(verbose_name='Букеты', blank=True, null=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая сумма', blank=True,
                                      null=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Flowers(models.Model):
    name_flower = models.CharField(verbose_name='Название цветка', max_length=120)
    image_flower = models.ImageField(verbose_name='Изображение цветка', upload_to='flowers/%Y/%m/%d')
    price = models.DecimalField(verbose_name='Цена за один цветок', max_digits=15, decimal_places=2)
    counts = models.IntegerField(verbose_name='Количество', default=1)

    def __str__(self):
        return self.name_flower

    class Meta:
        verbose_name = 'Цветок'
        verbose_name_plural = 'Цветы'


class Pack(models.Model):
    name_pack = models.CharField(verbose_name='Название обертки', max_length=120)
    pack = models.ImageField(verbose_name='Изображение обертки', upload_to='pack/%Y/%m/%d')
    price = models.DecimalField(verbose_name='Цена за обертку', max_digits=15, decimal_places=2)

    def __str__(self):
        return self.name_pack

    class Meta:
        verbose_name = 'Упаковка'
        verbose_name_plural = 'Упаковки'


class Decoration(models.Model):
    name_decoration = models.CharField(verbose_name='Название украшения', max_length=120)
    decoration = models.ImageField(verbose_name='Изображение украшения', upload_to='decoration/%Y/%m/%d')
    price = models.DecimalField(verbose_name='Цена за украшение', max_digits=15, decimal_places=2)

    def __str__(self):
        return self.name_decoration

    class Meta:
        verbose_name = 'Украшение'
        verbose_name_plural = 'Украшения'


class Bouquet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    flowers = models.JSONField()

    name_pack = models.CharField(max_length=255, blank=True, null=True)
    name_decoration = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = 'Букет клиента'
        verbose_name_plural = 'Букеты клиентов'


class UserBouquetOrder(models.Model):
    order_status = models.CharField(
        verbose_name='Статус доставки',
        max_length=50,
        choices=[
            ('decorated', 'Оформлен'),
            ('delivery', 'В пути'),
            ('delivered', 'Доставлен'),
        ],
        default='decorated'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bouquet = models.ForeignKey('Bouquet', on_delete=models.CASCADE)
    name_pack = models.CharField(max_length=255, blank=True, null=True)
    name_decoration = models.CharField(max_length=500, blank=True, null=True)
    flowers = models.JSONField(blank=True, null=True)
    sender_name = models.CharField(
        verbose_name='Имя отправителя',
        max_length=150,
        validators=[
            RegexValidator(
                regex='^[А-Яа-яЁё]+$',
                message='Используйте только русские символы.'
            )
        ],
        null=True
    )
    phone_number = models.CharField(verbose_name='Номер телефона отправителя', max_length=20, null=True)
    recipient_name = models.CharField(
        verbose_name='Имя получателя',
        max_length=150,
        validators=[
            RegexValidator(
                regex='^[А-Яа-яЁё]+$',
                message='Используйте только русские символы.'
            )
        ],
        null=True
    )
    recipient_phone = models.CharField(verbose_name='Номер телефона получателя', max_length=20, null=True)
    delivery_type = models.CharField(verbose_name='Тип доставки', max_length=50, choices=[
        ('pickup', 'Самовывоз'),
        ('courier', 'Доставка курьером'),
    ])

    address = models.CharField(max_length=255)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True)

    pay_type = models.CharField(verbose_name='Тип оплаты', max_length=50, choices=[
        ('cash', 'Наличными'),
        ('card', 'Картой при получении'),
        ('online', 'Оплатить онлайн'),
    ])
    card_number = models.CharField(verbose_name='Номер карты', max_length=20, null=True, blank=True)
    CVV = models.CharField(verbose_name='Защитный код с обратной стороны', max_length=20, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = 'Заказ клиентского букета'
        verbose_name_plural = 'Заказы клиентских букетов'


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    message = models.CharField(verbose_name='Сообщение', max_length=255, null=True)
    image = models.ImageField(verbose_name='Изображение цветка', upload_to='answer/%Y/%m/%d', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Answer(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    answer = models.CharField(verbose_name='Ответ', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
