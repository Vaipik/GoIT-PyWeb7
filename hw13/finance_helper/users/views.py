from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, decorators
from django.urls import reverse_lazy
from django.views.generic import View, CreateView

from . import forms


class SignInAjax(View):

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse(data={"status": 201}, status=201)
            return JsonResponse(
                data={
                    "error": "Username and(or) password not valid",
                    "status": 400
                },
                status=200
            )
        return JsonResponse(
            data={
                "error": "Enter username and password",
                "status": "400"
            },
            status=400)


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
