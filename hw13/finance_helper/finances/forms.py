from django import forms

from .libs import constants
from . import models


class AddTransactionForm(forms.Form):
    description = forms.CharField(
        max_length=constants.DESCRIPTION_MAX_LENGTH,
        min_length=constants.DESCRIPTION_MIN_LENGTH,
    )
    amount = forms.DecimalField(
        max_digits=constants.DECIMAL_MAX_DIGITS,
        decimal_places=constants.DECIMAL_PLACES
    )


class AddAccountForm(forms.ModelForm):
    name = forms.CharField(
        max_length=constants.ACCOUNT_MAX_LENGTH,
        min_length=constants.ACCOUNT_MIN_LENGTH,
    )
    balance = forms.DecimalField(
        max_digits=constants.DECIMAL_MAX_DIGITS,
        decimal_places=constants.DECIMAL_PLACES
    )

    class Meta:
        model = models.Account
        fields = ["name", "balance"]
