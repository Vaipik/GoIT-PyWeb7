from django.shortcuts import render, get_object_or_404, redirect

from . import forms
from . import models


def index(request):

    user = request.user
    context = {}
    if user.is_authenticated:
        accounts: list[models.Account] = models.Account.objects.filter(user=user).all()
        context["accounts"] = accounts

    return render(
        request,
        "finances/pages/index.html",
        context
    )


def add_account(request):

    if request.method == "POST":
        form = forms.AddAccountForm(request.POST)
        if form.is_valid():
            models.Account(
                name=form.cleaned_data["name"],
                balance=form.cleaned_data["balance"],
                user=request.user
            ).save()
            return redirect("finances:index")

    form = forms.AddAccountForm()
    return render(request, "finances/pages/add_account.html", {"form": form})


def show_account(request, acc_url):

    transactions = models.Transaction.objects.filter(account__slug=acc_url).all()
    print(transactions)
    context = {
        "acc_url": acc_url,
        "transactions": transactions
    }

    return render(
        request,
        "finances/pages/show_account.html",
        context
    )


def delete_account(request, acc_url: str):
    if request.method == "POST":
        pass
        # account = models.Account.objects.get(name=)


def add_transaction(request, acc_url: str):

    account: models.Account = models.Account.objects.get(slug=acc_url)
    if request.method == "POST":
        form = forms.AddTransactionForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data["description"]
            amount = form.cleaned_data["amount"]
            category = form.data.get("category", "No category")

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


def check_category(name: str):
    category = models.Category.objects.filter(name=name).first()
    return category


def delete_transaction(request, trans_url):
    pass


def edit_transaction(request, trans_url):
    pass


def get_transaction(request, trans_url):
    transaction = get_object_or_404(models.Transaction, slug=trans_url, user=request.user)
    return transaction
