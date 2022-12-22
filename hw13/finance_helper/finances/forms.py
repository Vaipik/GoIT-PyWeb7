from django import forms

from .libs import constants


class AddTransactionForm(forms.Form):

    description = forms.CharField(
        max_length=constants.DESCRIPTION_MAX_LENGTH,
        min_length=constants.DESCRIPTION_MIN_LENGTH,
    )
    amount = forms.DecimalField(
        max_digits=constants.DECIMAL_MAX_DIGITS,
        decimal_places=constants.DECIMAL_PLACES
    )
    category = forms.CharField(
        max_length=constants.CATEGORY_MAX_LEGNTH,
        min_length=constants.CATEGORY_MIN_LEGNTH
    )