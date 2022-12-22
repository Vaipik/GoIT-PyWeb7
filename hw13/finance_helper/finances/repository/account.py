from django.contrib.auth.models import User

from finance_helper.finances.models import Account


class AccountCRUD:

    def get_choices(self, user: User) -> tuple[tuple]:
        accounts = Account.objects.filter(user=user)
