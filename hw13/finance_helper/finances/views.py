from decimal import Decimal, InvalidOperation

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, View
from django.views.generic.base import ContextMixin

from . import forms
from . import models
from .utils import UserDataMixin


class AboutPageView(UserDataMixin, TemplateView):
    template_name = "finances/pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_data(title="About website")  # updating context
        )
        return context


class HomePageView(UserDataMixin, ListView):
    template_name = "finances/pages/index.html"
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_data(
                title="Main page",
                page_obj=context["page_obj"]
            )
        )
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            transactions = models.Transaction.objects. \
                select_related("account"). \
                filter(account__user=user)
            trans_by_acc = {}
            for transaction in transactions:
                trans_by_acc.setdefault(
                    transaction.account, []
                ).append(transaction)

            return list(trans_by_acc.items())
        return []

class AccountCreateView(UserDataMixin, LoginRequiredMixin, CreateView):
    model = models.Account
    form_class = forms.AccountForm
    template_name = "finances/pages/add_account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_data(title="New account creation")  # updating context
        )
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AccountEditView(UserDataMixin, LoginRequiredMixin, UpdateView):
    template_name = "finances/pages/edit_account.html"
    form_class = forms.AccountForm
    slug_url_kwarg = "acc_url"
    model = models.Account

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_data(title="Editing account name"),  # updating context
            account=self.object
        )
        return context


class ShowAccountView(UserDataMixin, ListView):
    template_name = "finances/pages/show_account.html"
    slug_url_kwarg = "acc_url"
    paginate_by = 7

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_by = self.request.GET.get("order_by")
        if order_by:
            paginator, page_obj, is_paginated, object_list = self.paginate_queryset(
                self.__order_queryset(order_by), 7
            )
            context["paginator"] = paginator
            context["page_obj"] = page_obj
            context["is_paginated"] = is_paginated
            context["object_list"] = object_list
            context["order_by"] = order_by

        context.update(
            self.get_user_data(
                page_obj=context["page_obj"],
                account=models.Account.objects.get(slug=self.kwargs["acc_url"])
            )
        )

        return context

    def get_queryset(self):
        return models.Transaction.objects. \
            select_related("account"). \
            filter(
                account__slug=self.kwargs["acc_url"],
                account__user=self.request.user
            )

    def __order_queryset(self, order_by: str):
        _key = order_by.replace(" ", "_").lower()
        queryset = self.get_queryset()
        _orderings = {
            "description": queryset.order_by("-description"),
            "amount": queryset.order_by("-amount"),
            "category": queryset.order_by("-category"),
            "remaining balance": queryset.order_by("-balance")
        }
        return _orderings.get(_key, queryset)


class TransactionCreateView(ContextMixin, UserDataMixin, LoginRequiredMixin, View):
    template_name = "finances/pages/add_transaction.html"
    slug_url_kwarg = "acc_url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_data(),
            account=models.Account.objects.get(slug=self.kwargs["acc_url"]),
            title="Creating new transaction",
        )
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(form=forms.AddTransactionForm)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = forms.AddTransactionForm(request.POST)
        context = self.get_context_data(form=form)
        if form.is_valid():
            description = form.cleaned_data["description"]
            amount = form.cleaned_data["amount"]

            category = request.POST.get("categories")
            category = "No category" if not category else category
            checked_category = check_category(category)
            if checked_category is None:
                category = models.Category(name=category)
                category.save()
            else:
                category = checked_category
            category.transaction_set.create(
                description=description,
                amount=amount,
                account=context["account"]
            )

            return redirect("finances:show_account", acc_url=self.kwargs["acc_url"])
        return render(request, self.template_name, context)


class TransactionEditView(ContextMixin, UserDataMixin, LoginRequiredMixin, View):
    template_name = "finances/pages/edit_transaction.html"
    slug_url_kwarg = "acc_url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_data(),
            account=models.Account.objects.get(slug=self.kwargs["acc_url"]),
            title="Editing transaction data",
        )
        return context

    def get(self, request, *args, **kwargs):
        transaction = models.Transaction.objects.get(slug=kwargs["trans_url"])
        context = self.get_context_data(
            form=forms.EditTransactionForm(initial=vars(transaction)),
            transaction=transaction
        )
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = forms.EditTransactionForm(request.POST)
        context = self.get_context_data(form=form)
        if form.is_valid():
            transaction = models.Transaction.objects.get(slug=kwargs["trans_url"])
            transaction.description = form.cleaned_data["description"]
            transaction.amount = form.cleaned_data["amount"]
            transaction.date = form.cleaned_data["date"]
            transaction.save()
            return redirect("finances:show_account", kwargs["acc_url"])

        return render(request, self.template_name, context)


@login_required
def delete_account(request, acc_url: str):
    if request.method == "POST":
        models.Account.objects.get(slug=acc_url).delete()

    return redirect("finances:index")


@login_required
def delete_transaction(request, acc_url, trans_url):
    transaction: models.Transaction = models.Transaction.objects.get(slug=trans_url)
    transaction.delete()
    user = request.user
    return redirect("finances:show_account", acc_url=acc_url)


class CategoryPageView(UserDataMixin, ListView):
    template_name = "finances/pages/trans_by_cat.html"
    paginate_by = 3
    slug_url_kwarg = "cat_url"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_data(
                title="Category page",
                page_obj=context["page_obj"]
            )
        )
        return context

    def get_queryset(self):
        transactions = models.Transaction.objects. \
            select_related("category"). \
            filter(account__user=self.request.user)
        trans_by_acc = {}
        for transaction in transactions:
            if transaction.category.slug == self.kwargs["cat_url"]:
                trans_by_acc.setdefault(
                    transaction.account, []
                ).append(transaction)

        return list(trans_by_acc.items())


class SearchPageView(UserDataMixin, ListView):
    template_name = "finances/pages/search.html"
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_data(
                title="Search page",
                page_obj=context["page_obj"]
            )
        )
        return context

    def get_queryset(self):
        request_data = self.request.GET.get("search")
        print(request_data)
        words, numbers = self.__parse_search_request(request_data)
        transactions = models.Transaction.objects \
            .filter(account__user=self.request.user) \
            .select_related("category")

        # Dictionary with account as key and set of matched transactions as value
        matched_transactions = {}
        if numbers:
            for transaction in transactions:
                if transaction.amount in numbers:
                    matched_transactions.setdefault(
                        transaction.account, set()  # set is required to prevent doubling
                    ).add(transaction)

        if words:

            for word in words:
                for transaction in transactions:
                    if word in transaction.description:
                        matched_transactions.setdefault(
                            transaction.account, set()  # set is required to prevent doubling
                        ).add(transaction)

        for acc in matched_transactions:
            matched_transactions[acc] = list(matched_transactions.get(acc))  # convert set to list
        return list(matched_transactions.items())

    @staticmethod
    def __parse_search_request(request_data) -> tuple[list[str], list[Decimal]]:
        """
        Splitting search data into numbers and words.
        :param request_data: search field input data
        :return: One tuple contains two lists.
        """
        numbers = []
        words = []

        for item in request_data.split():
            try:
                numbers.append(Decimal(item))
            except InvalidOperation:
                pass

            if item.isalpha():
                words.append(item)

        return words, numbers


def check_category(name: str) -> models.Category | None:
    """
    Each category has unique url thus this function checks is cat existing or not.
    :param name: category name
    :return: Category instance if it exists or None.
    """
    return models.Category.objects.filter(name=name).first()
