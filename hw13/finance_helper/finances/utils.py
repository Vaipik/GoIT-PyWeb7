from . import models
from .libs.correlate_pagination import transactions_for_acc


class UserDataMixin:
    """
    This mixin is used to query from db user categories and accounts
    """
    def get_user_data(self, **kwargs):
        context = kwargs
        user = self.request.user
        accounts = models.Account.objects.filter(user=user)
        categories = models.Category.objects.filter(transaction__account__user=user)
        context["accounts"] = accounts
        context["categories"] = categories

        return context

    def get_filled_user_acc(self, **kwargs):
        context = kwargs
        user = self.request.user
        transactions = models.Transaction.objects.select_related("user").filter(account__user=user)
        context["transactions"] = transactions

        return context

