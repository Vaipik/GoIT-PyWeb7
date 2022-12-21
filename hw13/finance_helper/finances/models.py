from django.db import models

from .libs import constants


class Category(models.Model):

    name = models.CharField(
        max_length=constants.CATEGORY_MAX_LEGNTH,
        unique=True,
        null=False,
        verbose_name="Category"
    )


class Transactions(models.Model):

    description = models.CharField(
        max_length=constants.DESCRIPTION_MAX_LENGTH,
        blank=True,
        verbose_name="Description"
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=""
    )
    amount = models.DecimalField(
        decimal_places=constants.DECIMAL_PLACES,
        verbose_name=""
    )
    is_income = models.BooleanField(

    )
    category = models.ForeignKey(
        to="Category",
        on_delete=models.SET_NULL,
    )

    class Meta:

        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-date", "-amount", "-description"]
