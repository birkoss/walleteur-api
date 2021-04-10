from datetime import timedelta

from django.http import HttpResponse
from django.utils import timezone

from core.helpers import add_months

from .models import ScheduledTransaction, Transaction


def scheduled_transactions(request):
    scheduled_transactions = ScheduledTransaction.objects.filter(
        date_next_due__lte=timezone.now()
    )

    for schedule_transaction in scheduled_transactions:
        # Create a NEW transactions
        transaction = Transaction(
            type='S',
            amount=schedule_transaction.amount,
            reason=schedule_transaction.reason,
            person=schedule_transaction.person,
            scheduled_transaction=schedule_transaction,
        )
        transaction.save()

        # Update the next due date for this schedule transaction
        if schedule_transaction.interval_type == 'daily':
            next_due_date = schedule_transaction.date_next_due + timedelta(
                days=schedule_transaction.interval_amount
            )
        else:
            next_due_date = add_months(
                schedule_transaction.date_next_due,
                schedule_transaction.interval_amount
            )

        schedule_transaction.date_next_due = next_due_date
        schedule_transaction.save()

        # Update person balance to reflect the new transaction
        schedule_transaction.person.update_balance()

    return HttpResponse("Transactions: " + str(len(scheduled_transactions)))
