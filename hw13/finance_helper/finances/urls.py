from django.urls import path

from . import views


app_name = "finances"

urlpatterns = [
    path("", views.index, name="index"),
    # path("about/", views.about, name="about"),
    path("about/", views.AboutPageView.as_view(), name="about"),
    path("add_account/", views.AccountCreateView.as_view(), name="add_account"),
    path("delete_account/<slug:acc_url>", views.delete_account, name="delete_account"),
    path("edit_account/<slug:acc_url>", views.edit_account, name="edit_account"),
    path("category/<slug:cat_url>", views.show_transactions_by_category, name="show_transactions_by_category"),
    path(r"search/", views.search, name="search"),
    path("<slug:acc_url>/", views.show_account, name="show_account"),
    path("<slug:acc_url>/add_transaction/", views.add_transaction, name="add_transaction"),
    path("<slug:acc_url>/delete_transaction/<slug:trans_url>/", views.delete_transaction, name="delete_transcation"),
    path("<slug:acc_url>/edit_transaction/<slug:trans_url>/", views.edit_transaction, name="edit_transaction"),

]
