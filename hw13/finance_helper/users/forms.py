from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .libs import constants


class RegistrationForm(UserCreationForm):

    username = forms.CharField(
        min_length=constants.USERNAME_MINLENGTH,
        max_length=constants.USERNAME_MAXLENGTH,
    )
    password1 = forms.CharField(
        min_length=constants.PASSWORD_MINLENGTH,
        max_length=constants.PASSWORD_MAXLENGTH,
        required=True,
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        min_length=constants.PASSWORD_MINLENGTH,
        max_length=constants.PASSWORD_MAXLENGTH,
        required=True,
        widget=forms.PasswordInput()
    )


    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
