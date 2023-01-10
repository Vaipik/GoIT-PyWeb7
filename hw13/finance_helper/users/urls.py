from django.urls import path

from . import views


app_name = "users"

urlpatterns = [
    path("registration/", views.SignUpView.as_view(), name="sign_up"),
    path("login/", views.SignInAjax.as_view(), name="sign_in_ajax"),
    path("logout/", views.sign_out, name="sign_out")
]

