from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, decorators

from .forms import RegistrationForm, LoginForm


def sign_in(request):
    user = request.user
    form = LoginForm()

    if user.is_authenticated:
        return redirect("finances:index")

    if request.method == "POST":
        user = authenticate(
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user is None:
            return redirect("users:sign_in")

        login(request, user)
        return redirect("finances:index")

    context = {
        "form": form,
    }

    return render(request, "users/login.html", context)


@decorators.login_required
def sign_out(request):
    logout(request)
    return redirect("finances:index")


def sign_up(request):
    form = RegistrationForm()

    if request.user.is_authenticated:
        return redirect("finances:index")

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("users:sign_in")

    context = {
        "form": form,
        "title": "Registration page",
    }
    return render(request, "users/register.html", context)
