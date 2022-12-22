from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from . import forms
from . import models


def index(request):
    return render(
        request,
        "finances/pages/index.html"
    )


def add_transaction(request):

    if request.method == "POST":
        form = forms.AddTransactionForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data["description"]
            amount = form.cleaned_data["amount"]
            user = request.user

            category = form.cleaned_data["category"]
            checked_category = check_category(category)
            if checked_category is None:
                category = models.Category(name=category)
                category.save()
            else:
                category = checked_category
            models.Transaction(
                description=description,
                amount=amount,
                user=user,
                category=category
            ).save()

            return redirect("finances:index")

    form = forms.AddTransactionForm()

    context = {
        "form": form,
        "user": request.user,
    }

    return render(
        request,
        "finances/pages/add_transaction.html",
        context
    )


def check_category(name: str):
    category = models.Category.objects.filter(name=name).first()
    return category if category else None


def delete_transaction(request, slug_url):
    pass


def edit_transaction(request, slug_url):
    pass


def get_transaction(request, slug_url):
    transaction = get_object_or_404(models.Transaction, slug=slug_url, user=request.user)
    return transaction
