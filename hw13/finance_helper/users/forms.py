from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .libs import constants


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        min_length=constants.USERNAME_MINLENGTH,
        max_length=constants.USERNAME_MAXLENGTH,
        label="Enter username",
        widget=forms.TextInput(
            attrs={
                "class": "form-control mt-3",
            }
        )
    )
    password1 = forms.CharField(
        min_length=constants.PASSWORD_MINLENGTH,
        max_length=constants.PASSWORD_MAXLENGTH,
        required=True,
        label="Enter password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mt-3",
                "placeholder": "123456789Aa!1",
            }
        )
    )
    password2 = forms.CharField(
        min_length=constants.PASSWORD_MINLENGTH,
        max_length=constants.PASSWORD_MAXLENGTH,
        required=True,
        label="Repeat password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mt-3",
                "placeholder": "123456789Aa!1",
            }
        )
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        min_length=constants.USERNAME_MINLENGTH,
        max_length=constants.USERNAME_MAXLENGTH,
        label="Enter username",
        widget=forms.TextInput(
            attrs={
                "class": "form-control mt-3",
            }
        )
    )
    password = forms.CharField(
        min_length=constants.PASSWORD_MINLENGTH,
        max_length=constants.PASSWORD_MAXLENGTH,
        required=True,
        label="Enter password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mt-3",
                "placeholder": "123456789Aa!1",
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'password']
