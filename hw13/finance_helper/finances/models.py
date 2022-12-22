from django.db import models
from django.contrib.auth.models import User

from autoslug import AutoSlugField

from .libs import constants


class Category(models.Model):

    name = models.CharField(
        max_length=constants.CATEGORY_MAX_LEGNTH,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Category"
    )
    slug = AutoSlugField(
        populate_from="name",
        unique=True,
        max_length=constants.CATEGORY_MAX_URL
    )

    def __str__(self):
        return self.name


class Transactions(models.Model):

    description = models.CharField(
        max_length=constants.DESCRIPTION_MAX_LENGTH,
        blank=True,
        null=True,
        verbose_name="Description"
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date"
    )
    amount = models.DecimalField(
        max_digits=constants.DECIMAL_MAX_DIGITS,
        decimal_places=constants.DECIMAL_PLACES,
        verbose_name="Value, UAH"
    )
    is_costs = models.BooleanField(
        verbose_name="Costs"
    )
    balance = models.DecimalField(
        max_digits=constants.DECIMAL_MAX_DIGITS,
        decimal_places=constants.DECIMAL_PLACES,
        default=0,
        verbose_name="Remaining balance"
    )
    slug = AutoSlugField(
        unique=True,
        max_length=constants.DESCRIPTION_MAX_URL,
        unique_with=("description", "user")
    )
    category = models.ForeignKey(
        to="Category",
        on_delete=models.SET_NULL,
        null=True
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )

    class Meta:

        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-date", "-amount", "-description"]

    def __str__(self):
        return self.description if len(self.description) < 30 else self.description[:30] + "..."
