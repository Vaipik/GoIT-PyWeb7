from django.db.models import QuerySet, Subquery, OuterRef
from django.shortcuts import render, redirect

from . import forms
from . import models
from .libs.ordering import order_by
from .libs.search_parser import parse_search_request


def index(request):

    user = request.user
    context = {}
    if user.is_authenticated:
        user_data: QuerySet = models.Transaction.objects.prefetch_related("account", "category").filter(account__user=user)
        accounts = models.Account.objects.filter(user=user)

        filled_accounts = {}
        for tr in user_data:
            filled_accounts.setdefault(tr.account, []).append(tr)

        for acc, trans in filled_accounts.items():
            for t in trans:
                print(acc, t.date, t.description)

        context = {
            "accounts": accounts,
            "categories": {tr.category for tr in user_data},
            "filled_accounts": filled_accounts,
        }

    return render(
        request,
        "finances/pages/index.html",
        context
    )


def add_account(request):

    if request.method == "POST":
        form = forms.AccountForm(request.POST)
        if form.is_valid():
            models.Account(
                name=form.cleaned_data["name"],
                balance=form.cleaned_data["balance"],
                user=request.user
            ).save()
            return redirect("finances:index")

    form = forms.AccountForm()
    return render(request, "finances/pages/add_account.html", {"form": form})


def edit_account(request, acc_url: str):
    account = models.Account.objects.get(slug=acc_url)
    form = forms.AccountForm(instance=account)
    context = {"account": account, "form": form}

    if request.method == "POST":
        form = forms.AccountForm(request.POST)
        if form.is_valid():
            account.name = form.cleaned_data["name"]
            account.balance = form.cleaned_data["balance"]
            account.save()
            return redirect("finances:show_account", acc_url=acc_url)

        context["form"] = form

    return render(request, "finances/pages/edit_account.html", context)


def delete_account(request, acc_url: str):
    if request.method == "POST":
        models.Account.objects.get(slug=acc_url).delete()
        return redirect("finances:index")


def show_account(request, acc_url):

    transactions = models.Transaction.objects.filter(account__slug=acc_url).all()
    account = models.Account.objects.get(slug=acc_url)

    order_by_key = request.GET.get("order_by")
    ordered_data = order_by(order_by_key)

    context = {
        "acc_url": acc_url,
        "transactions": ordered_data(transactions),
        "account": account
    }

    return render(
        request,
        "finances/pages/show_account.html",
        context
    )


def add_transaction(request, acc_url: str):

    account: models.Account = models.Account.objects.get(slug=acc_url)
    if request.method == "POST":
        form = forms.AddTransactionForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data["description"]
            amount = form.cleaned_data["amount"]

            category = request.POST.get("category")
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
                account=account
            )

            return redirect("finances:show_account", acc_url=acc_url)

    form = forms.AddTransactionForm()
    categories = models.Category.objects.all()
    print(categories)
    context = {
        "form": form,
        "categories": categories,
        "account": account
    }

    return render(
        request,
        "finances/pages/add_transaction.html",
        context
    )


def edit_transaction(request, acc_url: str, trans_url: str):

    transaction: models.Transaction = models.Transaction.objects.get(slug=trans_url)
    form = forms.EditTransactionForm(instance=transaction)

    if request.method == "POST":

        form = forms.EditTransactionForm(request.POST)
        if form.is_valid():

            transaction.description = form.cleaned_data["description"]
            transaction.amount = form.cleaned_data["amount"]
            transaction.date = form.cleaned_data["date"]
            transaction.save()
            return redirect("finances:show_account", acc_url)

    context = {
        "acc_url": acc_url,
        "transaction": transaction,
        "form": form,
        "categories": models.Category.objects.all(),
        "account": models.Account.objects.get(slug=acc_url)
    }
    return render(request, "finances/pages/edit_transaction.html", context)


def delete_transaction(request, acc_url, trans_url):
    transaction: models.Transaction = models.Transaction.objects.get(slug=trans_url)
    transaction.delete()
    return redirect("finances:show_account", acc_url=acc_url)


def check_category(name: str):
    return models.Category.objects.filter(name=name).first()


def search(request):
    request_data = request.GET.get("search")
    words, numbers = parse_search_request(request_data)
    user = request.user
    context = {}

    if numbers:
        context["transactions"] = models.Transaction.objects.filter(
            amount__in=numbers,
            account__user=user
        )

    if words:

        for word in words:
            query: QuerySet = models.Transaction.objects.filter(
                description__contains=word,
                account__user=user
            )
            context["transactions"] = context.get("transactions", query) | query

    return render(request, "finances/pages/search.html", context)
