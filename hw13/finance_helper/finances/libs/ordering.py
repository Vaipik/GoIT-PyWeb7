def order_by_description(queryset):
    return queryset.order_by("-description")


def order_by_date(queryset):
    return queryset.order_by("-date")


def order_by_category(queryset):
    return queryset.order_by("-category")


def order_by_amount(queryset):
    return queryset.order_by("-amount")


def order_by_remaining(queryset):
    return queryset.order_by("-balance")


def order_by(url_query: str):

    key = url_query.replace(" ", "_").lower() if url_query is not None else "date"

    _dict = {
        "description": order_by_description,
        "date": order_by_date,
        "amount": order_by_amount,
        "category": order_by_category,
        "remaining_balance": order_by_remaining,
    }
    return _dict.get(key, order_by_date)
