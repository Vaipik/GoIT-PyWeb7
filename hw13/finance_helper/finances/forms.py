from django import forms

from .libs import constants
from . import models


class AddTransactionForm(forms.Form):
    description = forms.CharField(
        max_length=constants.DESCRIPTION_MAX_LENGTH,
        min_length=constants.DESCRIPTION_MIN_LENGTH,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    amount = forms.DecimalField(
        max_digits=constants.DECIMAL_MAX_DIGITS,
        decimal_places=constants.DECIMAL_PLACES,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    # class Meta:
    #     model = models.Transaction
    #     fields = ["description", "amount"]


class EditTransactionForm(forms.ModelForm):
    description = forms.CharField(
        max_length=constants.DESCRIPTION_MAX_LENGTH,
        min_length=constants.DESCRIPTION_MIN_LENGTH,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    amount = forms.DecimalField(
        max_digits=constants.DECIMAL_MAX_DIGITS,
        decimal_places=constants.DECIMAL_PLACES,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = models.Transaction
        fields = ["description", "amount", "date"]

class AccountForm(forms.Form):
    name = forms.CharField(
        max_length=constants.ACCOUNT_MAX_LENGTH,
        min_length=constants.ACCOUNT_MIN_LENGTH,
        label="Enter account name"
    )
    balance = forms.DecimalField(
        max_digits=constants.DECIMAL_MAX_DIGITS,
        decimal_places=constants.DECIMAL_PLACES,
    )
