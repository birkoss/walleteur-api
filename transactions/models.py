from django.db import models
from django.db.models.fields.related import ForeignKey

from core.models import TimeStampedModel, UUIDModel


class Person(TimeStampedModel, UUIDModel, models.Model):
    name = models.CharField(max_length=150, default="")
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    user = ForeignKey(
        "users.User", blank=True, null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Transaction(TimeStampedModel, UUIDModel, models.Model):
    person = ForeignKey(Person, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    reason = models.CharField(
        max_length=200, null=True, blank=True, default=''
    )

    def __str__(self):
        return str(self.amount) + "$ -> " + self.person.name
