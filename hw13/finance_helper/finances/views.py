from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

from . import forms
from . import models


def index(request):
    return render(
        request,
        "finances/pages/index.html",
    )


def add_account(request):

    if request.method == "POST":
        form = forms.AddAccountForm(request.POST)
        if form.is_valid():
            pass

    form = forms.AddAccountForm()
    return render(request, "finances/pages/add_account.html", {"form": form})


def add_transaction(request):
    if request.method == "POST":
        form = forms.AddTransactionForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data["description"]
            amount = form.cleaned_data["amount"]
            user = request.user
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
            )

            return redirect("finances:index")

    form = forms.AddTransactionForm()
    categories = models.Category.objects.all()
    context = {
        "form": form,
        "user": request.user,
        "categories": categories
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
