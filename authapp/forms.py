from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class AuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Логин'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пароль'
        })


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'last_name',
            'first_name',
            'phone_number',
            'email',
            'username',
            'password1',
            'password2',
        )

    APPROVAL_CHOICES = [
        ('approval', 'Согласие на обработку персональных данных'),
    ]
    approval = forms.ChoiceField(
        choices=APPROVAL_CHOICES,
        widget=forms.RadioSelect,
        label='Согласие на обработку персональных данных'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, item in self.fields.items():
            item.widget.attrs['class'] = 'form-control'
            item.help_text = ''

        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Фамилия'
        })

        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Имя'
        })

        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Номер телефона'
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Электронная почта'
        })

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Логин'
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пароль'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Повтор пароля'
        })

        self.fields['approval'].widget.attrs.update({'class': 'form-check-input'})