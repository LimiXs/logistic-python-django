from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Note, TradeLogistic


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ0123456789- '
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Должны быть только русские буквы, дефис и пробел.'

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория')
    note = forms.ModelChoiceField(queryset=Note.objects.all(), required=False, label='Примечание')

    class Meta:
        model = TradeLogistic
        fields = ['title', 'slug', 'content', 'is_published', 'cat', 'tags', 'note']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
        }
        labels = {'slug': 'URL'}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов!')

        return title


class AddInvoiceTableForm(forms.Form):
    no = forms.IntegerField(label='№')
    product_code = forms.CharField(label='Код товара', max_length=10)
    name = forms.CharField(label='Наименование', max_length=100)
    vendor_code = forms.CharField(label='Артикул', max_length=100)
    brand = forms.CharField(label='Торговая марка', max_length=100)
    manufacturer = forms.CharField(label='Производитель', max_length=100)
    country = forms.CharField(label='Страна', max_length=100)
    unit_of_measure = forms.CharField(label='Ед. изм.', max_length=100)
    quantity_per_unit = forms.IntegerField(label='Кол-во в ед. изм.')
    price = forms.FloatField(label='Цена')
    cost = forms.FloatField(label='Стоимость')
    net_weight = forms.FloatField(label='Вес нетто')
    gross_weight = forms.FloatField(label='Вес брутто')
    additional_code = forms.CharField(label='Доп. код', max_length=4)


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))