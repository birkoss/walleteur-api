from django.db import models
from django.db.models import Sum
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

    def update_balance(self):
        total_transactions = Transaction.objects.filter(
            person=self
        ).aggregate(Sum('amount'))
        newBalance = total_transactions['amount__sum']

        if newBalance is None:
            newBalance = 0

        self.balance = newBalance
        self.save()


class TransactionData(TimeStampedModel, UUIDModel, models.Model):
    person = ForeignKey(Person, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    reason = models.CharField(
        max_length=200, null=True, blank=True, default=''
    )

    class Meta:
        abstract = True


class Transaction(TransactionData, models.Model):
    type = models.CharField(max_length=1, default='', null=False, blank=True)
    scheduled_transaction = models.ForeignKey(
        'transactions.ScheduledTransaction',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.amount) + "$ -> " + self.person.name


class ScheduledTransaction(TransactionData):
    INTERVAL_TYPES = [
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
    ]

    date_next_due = models.DateField()
    interval_amount = models.IntegerField(default=1)
    interval_type = models.CharField(
        max_length=10,
        choices=INTERVAL_TYPES,
        default='daily'
    )

    def __str__(self):
        return (
            str(self.amount) + "$ -> " + self.person.name
            + " (every " + str(self.interval_amount) + " "
            + ("day(s)" if self.interval_type == "daily" else "month(s)")
            + ")"
        )
