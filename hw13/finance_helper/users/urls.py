from django.urls import path

from . import views


app_name = "users"

urlpatterns = [
    path("registration/", views.sign_up, name="sign_up"),
    path("login/", views.sign_in, name="sign_in"),
    path("logout/", views.sign_out, name="sign_out")
]

