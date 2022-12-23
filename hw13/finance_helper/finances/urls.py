from django.urls import path

from . import views


app_name = "finances"

urlpatterns = [
    path("", views.index, name="index"),
    path("add_account", views.add_account, name="add_account"),
    path("<slug:acc_url>/add_transaction/", views.add_transaction, name="add_transaction"),
    path("<slug:acc_url>/delete_transaction/<slug:trans_url>/", views.delete_transaction, name="delete_transcation"),
    path("<slug:acc_url>/edit_transaction/<slug:trans_url>/", views.edit_transaction, name="edit_transaction"),
    path("<slug:acc_url>/<slug:trans_url>/", views.get_transaction, name="show_transcation"),
]
