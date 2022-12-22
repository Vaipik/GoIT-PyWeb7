from django.urls import path

from . import views


app_name = "finances"

urlpatterns = [
    path("", views.index, name="index"),
    path("add_transaction/", views.add_transaction, name="add_transaction"),
    path("delete_transaction/<slug:slug_url>/", views.delete_transaction, name="delete_transcation"),
    path("edit_transaction/<slug:slug_url>/", views.edit_transaction, name="index"),
    path("<slug:slug_url>/", views.get_transaction, name="show_transcation"),
]
