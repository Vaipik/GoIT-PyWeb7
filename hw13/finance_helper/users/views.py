from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, decorators
from django.urls import reverse_lazy
from django.views.generic import CreateView

from . import forms


class SignInView(LoginView):
    form_class = forms.LoginForm
    template_name = "users/login.html"
    extra_context = {"title": "Authorization page"}

    def get_success_url(self):
        return reverse_lazy("finances:index")


class SignUpView(CreateView):
    template_name = "users/register.html"
    form_class = forms.RegistrationForm
    extra_context = {"title": "Registration page"}

    def get_success_url(self):
        return reverse_lazy("finances:index")


@decorators.login_required
def sign_out(request):
    logout(request)
    return redirect("finances:index")
