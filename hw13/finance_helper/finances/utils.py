from . import models


class UserDataMixin:
    """
    This mixin is used to query from db user categories and accounts
    """
    def get_user_data(self, **kwargs):
        context = kwargs
        user = self.request.user
        if user.is_authenticated:

            accounts = models.Account.objects.filter(user=user)
            categories = models.Category.objects.filter(transaction__account__user=user).distinct("name")
            context["accounts"] = accounts
            context["categories"] = categories

        page = context.get("page_obj")

        if page is not None:
            pages = page.paginator.get_elided_page_range(
                number=page.number,
                on_each_side=1,
                on_ends=1
            )
            context["pages"] = pages

        return context
