from typing import Any

from django.core.paginator import Paginator


def transactions_for_acc(*, request, transactions, acc_url: str = None) -> tuple[Any, Any]:
    """
    Matching transactions for each acc and performing pagination. pagination is performed by
    max 3 accs with max 5 last transactions for each acc. If it is used to view single account shows 5 transactions
    per page.
    :param request: django.HttpRequest object
    :param transactions: current queryset for your view
    :param acc_url: is this for single account or for general views
    :return: page object for iterating over one page, pages
    """
    if acc_url is None:
        trans_by_acc = {}

        for transaction in transactions:
            trans_by_acc.setdefault(
                transaction.account, []
            ).append(transaction)

        paginator = Paginator(list(trans_by_acc.items()), 3)  # to split transaction for each account
    else:
        transactions = [transaction for transaction in transactions if transaction.account.slug == acc_url]
        paginator = Paginator(transactions, 5)
    page_number = request.GET.get("page", 1)
    print(page_number)
    page_obj = paginator.get_page(page_number)
    pages = paginator.get_elided_page_range(
        number=page_number,
        on_each_side=1,
        on_ends=1
    )

    return page_obj, pages


def transactions_for_cat(*, request, transactions, category_url: str) -> tuple[Any, Any, Any]:
    """

    :param request: django.HttpRequest object
    :param transactions: queryset with all transactions for current user
    :param category_url: to find exact category
    :return:
    """
    trans_by_acc = {}
    for transaction in transactions:
        if transaction.category.slug == category_url:
            current_cat = transaction.category
            trans_by_acc.setdefault(
                transaction.account, []
            ).append(transaction)

    paginator = Paginator(list(trans_by_acc.items()), 3)  # to split transaction for each accountQ
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    pages = paginator.get_elided_page_range(
        number=page_number,
        on_each_side=1,
        on_ends=1
    )

    return current_cat, page_obj, pages


def transactions_for_search(*, request, matched_transactions: dict) -> tuple[Any, Any]:
    """
    Return paginator objects for matched transactions.
    :param request: django.HttpRequest object
    :param matched_transactions: dictionary with matched transactions for your view
    :return: page object for iterating over one page, pages
    """
    paginator = Paginator(list(matched_transactions.items()), 3)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    pages = paginator.get_elided_page_range(
        number=page_number,
        on_each_side=1,
        on_ends=1
    )
    print(page_obj)
    print(matched_transactions)
    return page_obj, pages
