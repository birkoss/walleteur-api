from django.urls import path

from . import views as transactions_views


urlpatterns = [
    path(
        'cron/scheduledTransactions',
        transactions_views.scheduled_transactions,
        name='cron_scheduled_transactions'
    ),
]
