from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .libs import constants


class RegistrationForm(UserCreationForm):

    username = forms.CharField(
        min_length=constants.USERNAME_MINLENGTH,
        max_length=constants.USERNAME_MAXLENGTH,
    )
    # password1 =