from django import forms

from .libs import constants
from . import models


class AddTransactionForm(forms.Form):
    description = forms.CharField(
        max_length=constants.DESCRIPTION_MAX_LENGTH,
        min_length=constants.DESCRIPTION_MIN_LENGTH,
        label="Enter description",
        widget=forms.TextInput(
            attrs={
                "class": "form-control mt-3",
                "placeholder": "movie tickets",
                "id": "description"
            }
        )
    )
    amount = forms.DecimalField(
        max_digits=constants.DECIMAL_MAX_DIGITS,
        decimal_places=constants.DECIMAL_PLACES,
        label="Enter amount",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control mt-3",
                "placeholder": "100.00",
                "id": "amount"
            }
        )
    )


class EditTransactionForm(forms.ModelForm):
    description = forms.CharField(
        max_length=constants.DESCRIPTION_MAX_LENGTH,
        min_length=constants.DESCRIPTION_MIN_LENGTH,
        label="Enter description",
        widget=forms.TextInput(
            attrs={
                "class": "form-control mt-3",
                "placeholder": "movie tickets",
                "id": "description"
            }
        )
    )
    amount = forms.DecimalField(
        max_digits=constants.DECIMAL_MAX_DIGITS,
        decimal_places=constants.DECIMAL_PLACES,
        label="Enter amount",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control mt-3",
                "placeholder": "100.00",
                "id": "amount"
            }
        )
    )
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control mt-3"
                   }
        )
    )

    class Meta:
        model = models.Transaction
        fields = ["description", "amount", "date"]


class AccountForm(forms.ModelForm):
    name = forms.CharField(
        max_length=constants.ACCOUNT_MAX_LENGTH,
        min_length=constants.ACCOUNT_MIN_LENGTH,
        label="Enter new account name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control mt-3",
                "placeholder": "Foo's car spents",
                "id": "name",
            }
        )

    )

    class Meta:
        model = models.Account
        fields = ["name"]
