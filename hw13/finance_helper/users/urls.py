from django.urls import path

from . import views


app_name = "users"

urlpatterns = [
    path("registration/", views.SignUpView.as_view(), name="sign_up"),
    path("login/", views.SignInView.as_view(), name="sign_in"),
    path("logout/", views.sign_out, name="sign_out")
]

