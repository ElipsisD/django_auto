import re

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

from autos.models import Spare


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


class AddSpareForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car'].empty_label = 'Не выбрано'

    class Meta:
        model = Spare
        fields = ('car', 'autodoc_URL', 'exist_URL')

    def clean_autodoc_URL(self):
        autodoc_URL = self.cleaned_data.get('autodoc_URL', None)
        exist_URL = self.cleaned_data.get('exist_URL', None)
        if not autodoc_URL and not exist_URL:
            raise ValidationError('Введите хотя бы одну ссылку!')
        pattern = r'https:\/\/www\.autodoc\.ru\/.+'
        if not autodoc_URL or not re.match(pattern, autodoc_URL):
            raise ValidationError('Неверная ссылка')
        return autodoc_URL

    def clean_exist_URL(self):
        autodoc_URL = self.cleaned_data.get('autodoc_URL', None)
        exist_URL = self.cleaned_data.get('exist_URL', None)
        if not autodoc_URL and not exist_URL:
            raise ValidationError('Введите хотя бы одну ссылку!')
        pattern = r'https:\/\/www\.exist\.ru\/.+'
        if not exist_URL or not re.match(pattern, exist_URL):
            raise ValidationError('Неверная ссылка')
        return exist_URL
