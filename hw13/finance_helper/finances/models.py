from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

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

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["-name"]

    def __str__(self):
        return self.name

    @classmethod
    def get_default_pk(cls):
        obj, created = cls.objects.get_or_create(name="No category")
        return obj.pk


class Transaction(models.Model):
    description = models.CharField(
        max_length=constants.DESCRIPTION_MAX_LENGTH,
        blank=True,
        verbose_name="Description"
    )
    date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Date",
    )
    amount = models.DecimalField(
        max_digits=constants.DECIMAL_MAX_DIGITS,
        decimal_places=constants.DECIMAL_PLACES,
        verbose_name="Value, UAH"
    )
    balance = models.DecimalField(
        max_digits=constants.DECIMAL_MAX_DIGITS,
        decimal_places=constants.DECIMAL_PLACES,
        verbose_name="Remaining balance",
        blank=True,
        null=True
    )
    is_costs = models.BooleanField(
        verbose_name="Costs"
    )
    slug = AutoSlugField(
        populate_from="description",
        unique=True,
        max_length=constants.DESCRIPTION_MAX_URL,
    )
    category = models.ForeignKey(
        to="Category",
        on_delete=models.SET_DEFAULT,
        default=Category.get_default_pk
    )
    account = models.ForeignKey(
        to="Account",
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-date"]

    def save(self, *args, **kwargs):

        self.is_costs = True if self.amount < 0 else False
        self.__balance_editing()
        self.account.save()  # call save method to account model
        super(Transaction, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):

        self.account.balance -= self.amount
        self.balance = self.account.balance
        self.account.save()  # call save me thod to account model
        super(Transaction, self).delete(*args, **kwargs)

    def __balance_editing(self):

        if self.balance is None:
            self.account.balance += self.amount

        else:
            previous_amount = Transaction.objects.select_related("account").get(pk=self.id).amount
            print(f"Prev: {previous_amount}, curr: {self.amount}")
            self.account.balance = self.account.balance - previous_amount + self.amount

        self.balance = self.account.balance

    def __str__(self):
        return self.description if len(self.description) < 30 else self.description[:30] + "..."


class Account(models.Model):

    name = models.CharField(
        max_length=constants.ACCOUNT_MAX_LENGTH,
        blank=False,
        null=True,
        verbose_name="Account name"
    )
    balance = models.DecimalField(
        max_digits=constants.DECIMAL_MAX_DIGITS,
        decimal_places=constants.DECIMAL_PLACES,
        verbose_name="Remaining balance",
        blank=True,
        default=0,
        null=False
    )
    slug = AutoSlugField(
        populate_from="name",
        unique=True,
        max_length=constants.ACCOUNT_MAX_URL,
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = "Account",
        verbose_name_plural = "Accounts"
        ordering = ["-name", "-balance"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("finances:show_account", kwargs={"acc_url": self.slug})
