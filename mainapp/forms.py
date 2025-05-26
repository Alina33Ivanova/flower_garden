from django import forms

from mainapp.models import Reviews, Order, Flowers, Pack, Decoration, Message, UserBouquetOrder


class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Оставить отзыв'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, item in self.fields.items():
            item.widget.attrs['class'] = f'form-control {name}'
            item.help_text = ''


class OrderForm(forms.ModelForm):
    DELIVERY_CHOICES = [
        ('pickup', 'Самовывоз'),
        ('courier', 'Доставка курьером'),
    ]
    delivery_type = forms.ChoiceField(
        choices=DELIVERY_CHOICES,
        widget=forms.RadioSelect,
        label='Тип доставки'
    )

    PAY_CHOICES = [
        ('cash', 'Наличными'),
        ('card', 'Картой при получении'),
        ('online', 'Оплатить онлайн'),
    ]

    pay_type = forms.ChoiceField(
        choices=PAY_CHOICES,
        widget=forms.RadioSelect,
        label='Тип оплаты'
    )

    class Meta:
        model = Order
        fields = ['sender_name', 'phone_number', 'recipient_name', 'recipient_phone', 'delivery_type', 'address',
                  'date', 'time', 'comment', 'pay_type', 'card_number', 'CVV']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, item in self.fields.items():
            item.widget.attrs['class'] = f'form-control {name}'
            item.help_text = ''

            self.fields['sender_name'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Имя отправителя'
            })

            self.fields['phone_number'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Номер телефона отправителя'
            })

            self.fields['recipient_name'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Имя получателя'
            })

            self.fields['recipient_phone'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Номер телефона получателя'
            })

            self.fields['address'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Введите адрес доставки'
            })

            self.fields['card_number'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Номер карты'
            })

            self.fields['CVV'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'CVV'
            })

            self.fields['delivery_type'].widget.attrs.update({'class': 'form-check-input'})
            self.fields['pay_type'].widget.attrs.update({'class': 'form-check-input'})

            self.fields['comment'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Введите комментарий к заказу'
            })


class BouquetForm(forms.Form):
    clarify = forms.BooleanField(required=False, label='Уточнить детали')

    flowers = forms.ModelMultipleChoiceField(
        queryset=Flowers.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Цветы'
    )
    pack = forms.ModelChoiceField(
        queryset=Pack.objects.all(),
        widget=forms.RadioSelect,
        label='Упаковка'
    )
    decorations = forms.ModelMultipleChoiceField(
        queryset=Decoration.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Украшения',
        required=False
    )


class UserBouquetOrderForm(forms.Form):
    name_pack = forms.CharField(max_length=255, required=False)
    name_decoration = forms.CharField(max_length=500, required=False)
    flowers = forms.CharField(widget=forms.HiddenInput(), required=False)
    sender_name = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    recipient_name = forms.CharField(max_length=255, required=True)
    recipient_phone = forms.CharField(max_length=20, required=True)
    address = forms.CharField(max_length=500, required=True)
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=True
    )
    comment = forms.CharField(required=False)
    card_number = forms.CharField(max_length=16, required=False)
    CVV = forms.CharField(max_length=3, required=False)

    DELIVERY_CHOICES = [
        ('pickup', 'Самовывоз'),
        ('courier', 'Доставка курьером'),
    ]
    delivery_type = forms.ChoiceField(
        choices=DELIVERY_CHOICES,
        widget=forms.RadioSelect,
        label='Тип доставки'
    )

    PAY_CHOICES = [
        ('cash', 'Наличными'),
        ('card', 'Картой при получении'),
        ('online', 'Оплатить онлайн'),
    ]
    pay_type = forms.ChoiceField(
        choices=PAY_CHOICES,
        widget=forms.RadioSelect,
        label='Тип оплаты'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if name == 'delivery_type' or name == 'pay_type':
                field.widget.attrs['class'] = 'form-check-input'
            if name == 'comment':
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = 'Введите комментарий к заказу'
            if name == 'date':
                field.widget.attrs['class'] = 'form-control'
            if name == 'time':
                field.widget.attrs['class'] = 'form-control'

                self.fields['sender_name'].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': 'Имя отправителя'
                })

                self.fields['phone_number'].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': 'Номер телефона отправителя'
                })

                self.fields['recipient_name'].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': 'Имя получателя'
                })

                self.fields['recipient_phone'].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': 'Номер телефона получателя'
                })

                self.fields['address'].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': 'Введите адрес доставки'
                })

                self.fields['card_number'].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': 'Номер карты'
                })

                self.fields['CVV'].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': 'CVV'
                })

                self.fields['delivery_type'].widget.attrs.update({'class': 'form-check-input'})
                self.fields['pay_type'].widget.attrs.update({'class': 'form-check-input'})

                self.fields['comment'].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': 'Введите комментарий к заказу'
                })


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 1, 'placeholder': 'Сообщение'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, item in self.fields.items():
            item.widget.attrs['class'] = f'form-control {name}'
            item.help_text = ''
