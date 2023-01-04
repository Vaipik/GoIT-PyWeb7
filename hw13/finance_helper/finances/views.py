from django.db.models import QuerySet
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from . import forms
from . import models
from .libs.ordering import order_by
from .libs.search_parser import parse_search_request
from .libs.correlate_pagination import transactions_for_acc, transactions_for_cat, transactions_for_search


def index(request):
    user = request.user
    context = {}
    if user.is_authenticated:

        accounts = models.Account.objects.filter(user=user)
        transactions = models.Transaction.objects.prefetch_related("category", "account").filter(account__user=user)

        page_obj, pages = transactions_for_acc(
            request=request,
            transactions=transactions,
        )

        context = {
            "accounts": accounts,
            "categories": {tr.category for tr in transactions},
            "page_obj": page_obj,
            "pages": pages,
            "title": f"{user} accounts"
        }

    return render(
        request,
        "finances/pages/index.html",
        context
    )


def about(request):
    user = request.user
    context = {"title": "About website"}
    if user.is_authenticated:
        accounts = models.Account.objects.filter(user=user)
        transactions = models.Transaction.objects.prefetch_related("category", "account").filter(account__user=user)

        context["accounts"] = accounts
        context["categories"] = {tr.category for tr in transactions}

    return render(request, "finances/pages/about.html", context)


@login_required
def add_account(request):
    user = request.user
    accounts = models.Account.objects.filter(user=user)
    transactions = models.Transaction.objects.select_related("category").filter(account__user=user)
    if request.method == "POST":
        form = forms.AccountForm(request.POST)
        if form.is_valid():
            account = models.Account(
                name=form.cleaned_data["name"],
                user=request.user
            )
            account.save()
            return redirect("finances:show_account", acc_url=account.slug)

    form = forms.AccountForm()
    context = {
        "form": form,
        "categories": {tr.category for tr in transactions},
        "accounts": accounts
    }
    return render(request, "finances/pages/add_account.html", context)


@login_required
def edit_account(request, acc_url: str):
    account = models.Account.objects.get(slug=acc_url)

    user = request.user
    accounts = models.Account.objects.filter(user=user)
    transactions = models.Transaction.objects.select_related("category").filter(account__user=user)

    form = forms.AccountForm(instance=account)

    if request.method == "POST":
        form = forms.AccountForm(request.POST)
        if form.is_valid():
            account.name = form.cleaned_data["name"]
            account.balance = form.cleaned_data["balance"]
            account.save()
            return redirect("finances:show_account", acc_url=acc_url)

    context = {
        "account": account,
        "form": form,
        "accounts": accounts,
        "categories": {tr.category for tr in transactions},
    }

    return render(request, "finances/pages/edit_account.html", context)


@login_required
def delete_account(request, acc_url: str):

    if request.method == "POST":
        models.Account.objects.get(slug=acc_url).delete()

    return redirect("finances:index")




@login_required
def show_account(request, acc_url):
    user = request.user
    transactions = models.Transaction.objects.prefetch_related("category").filter(account__user=user)
    user_cats = models.Category.objects.filter(transaction__account__user=user)

    accounts = models.Account.objects.filter(user=user)
    for account in accounts:
        if account.slug == acc_url:
            current_account = account

    # For different ordering
    order_by_key = request.GET.get("order_by")
    ordered_data = order_by(order_by_key)

    page_obj, pages = transactions_for_acc(
        request=request,
        transactions=ordered_data(transactions),
        acc_url=acc_url,
    )

    context = {
        "page_obj": page_obj,
        "pages": pages,
        "account": current_account,
        "title": f"Account - {current_account.name}",
        "accounts": accounts,
        "categories": {category for category in user_cats},
        "order_by": order_by_key,
    }

    return render(
        request,
        "finances/pages/show_account.html",
        context
    )


@login_required
def add_transaction(request, acc_url: str):
    user = request.user
    transactions = models.Transaction.objects.select_related("category").filter(account__slug=acc_url)
    accounts = models.Account.objects.filter(user=user)
    account = accounts.get(slug=acc_url)

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

    context = {
        "form": form,
        "account": account,
        "accounts": accounts,
        "categories": {tr.category for tr in transactions}
    }

    return render(
        request,
        "finances/pages/add_transaction.html",
        context
    )


@login_required
def edit_transaction(request, acc_url: str, trans_url: str):
    transaction: models.Transaction = models.Transaction.objects.get(slug=trans_url)
    form = forms.EditTransactionForm(instance=transaction)

    user = request.user
    transactions = models.Transaction.objects.select_related("category").filter(account__slug=acc_url)
    accounts = models.Account.objects.filter(user=user)
    account = accounts.get(slug=acc_url)

    if request.method == "POST":

        form = forms.EditTransactionForm(request.POST)
        if form.is_valid():
            transaction.description = form.cleaned_data["description"]
            transaction.amount = form.cleaned_data["amount"]
            transaction.date = form.cleaned_data["date"]
            transaction.save()
            return redirect("finances:show_account", acc_url)

    context = {
        "transaction": transaction,
        "form": form,
        "categories": {tr.category for tr in transactions},
        "account": account,
        "accounts": accounts
    }
    return render(request, "finances/pages/edit_transaction.html", context)


@login_required
def delete_transaction(request, acc_url, trans_url):
    transaction: models.Transaction = models.Transaction.objects.get(slug=trans_url)
    transaction.delete()
    return redirect("finances:show_account", acc_url=acc_url)


@login_required
def check_category(name: str):
    return models.Category.objects.filter(name=name).first()


@login_required
def show_transactions_by_category(request, cat_url):
    user = request.user
    transactions = models.Transaction.objects.select_related("category").filter(account__user=user)
    accounts = models.Account.objects.filter(user=user)
    current_category, page_obj, pages = transactions_for_cat(
        request=request,
        transactions=transactions,
        category_url=cat_url
    )

    context = {
        "title": f"Category- {current_category}",
        "page_obj": page_obj,
        "pages": pages,
        "categories": {tr.category for tr in transactions},
        "current_category": current_category,
        "accounts": accounts
    }
    return render(request, "finances/pages/trans_by_cat.html", context)


@login_required
def search(request):
    request_data = request.GET.get("search")
    print(request_data)
    words, numbers = parse_search_request(request_data)
    user = request.user

    user_cats = models.Category.objects.filter(transaction__account__user=user)
    accounts = models.Account.objects.filter(user=user)

    transactions: QuerySet = models.Transaction.objects \
        .filter(account__user=user) \
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

    page_obj, pages = transactions_for_search(
        request=request,
        matched_transactions=matched_transactions
    )

    context = {
        "page_obj": page_obj,
        "pages": pages,
        "title": "Search page",
        "accounts": accounts,
        "categories": {cat for cat in user_cats},
        "request_data": request_data
    }

    return render(request, "finances/pages/search.html", context)
