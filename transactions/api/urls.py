from django.urls import path

from . import views as api_views


urlpatterns = [
    path(
        'v1/persons',
        api_views.persons.as_view(),
        name='persons'
    ),
    path(
        'v1/person/<str:person_id>',
        api_views.person.as_view(),
        name='person'
    ),
    path(
        'v1/person/<str:person_id>/transactions',
        api_views.person_transactions.as_view(),
        name='person_transactions'
    ),
    path(
        'v1/transactions',
        api_views.transactions.as_view(),
        name='transactions'
    ),
    path(
        'v1/transaction/<str:transaction_id>',
        api_views.transaction.as_view(),
        name='transaction'
    ),
]
