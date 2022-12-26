from django.shortcuts import render, redirect

from . import forms
from . import models


def index(request):

    user = request.user
    context = {}
    if user.is_authenticated:
        accounts = models.Account.objects.filter(user=user).all()
        context["accounts"] = accounts

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


def show_account(request, acc_url):

    transactions = models.Transaction.objects.filter(account__slug=acc_url).all()
    account = transactions.first()
    context = {
        "acc_url": acc_url,
        "transactions": transactions,
        "account": account
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


def check_category(name: str):
    return models.Category.objects.filter(name=name).first()


def delete_transaction(request, acc_url, trans_url):
    transaction: models.Transaction = models.Transaction.objects.get(slug=trans_url)
    transaction.delete()
    return redirect("finances:show_account", acc_url=acc_url)
