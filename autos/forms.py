import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from autos.models import Spare


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={"class": "form-input"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-input"}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={"class": "form-input"}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={"class": "form-input"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"}))


class AddSpareForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["car"].empty_label = "Не выбрано"

    class Meta:
        model = Spare
        fields = ("car", "autodoc_URL", "exist_URL")

    def clean(self) -> None:
        cleaned_data = super().clean()
        autodoc_url = cleaned_data.get("autodoc_URL", None)
        exist_url = cleaned_data.get("exist_URL", None)
        if not autodoc_url and not  exist_url:
            msg = "Введите хотя бы одну ссылку!"
            raise ValidationError(msg)

    def clean_autodoc_URL(self):
        autodoc_url = self.cleaned_data.get("autodoc_URL", None)
        pattern = r"https:\/\/www\.autodoc\.ru\/.+"
        if autodoc_url and not re.match(pattern, autodoc_url):
            msg = "Неверная ссылка"
            raise ValidationError(msg)
        return autodoc_url

    def clean_exist_URL(self):
        exist_url = self.cleaned_data.get("exist_URL", None)
        pattern = r"https:\/\/www\.exist\.ru\/.+"
        if exist_url and not re.match(pattern, exist_url):
            msg = "Неверная ссылка"
            raise ValidationError(msg)
        return exist_url
