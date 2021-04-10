from datetime import timedelta

from django.db.models import Count, Sum, Q
from django.utils import timezone

from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Person, ScheduledTransaction, Transaction

from core.helpers import create_error_response

from .serializers import (
    PersonSerializer, TransactionReadSerializer,
    ScheduledTransactionSerializer, PersonWriteSerializer,
    ScheduledTransactionWriteSerializer, TransactionWriteSerializer
)


class person(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, person_id, format=None):
        person = get_persons(
            user=request.user, id=person_id
        ).first()
        if person is None:
            return create_error_response('invalid_user')

        serializer = PersonSerializer(instance=person)

        return Response({
            'person': serializer.data,
            # @TODO: Remove when the next update is online
            'weeklyStats': {},
        }, status=status.HTTP_200_OK)

    def delete(self, request, person_id, format=None):
        person = Person.objects.filter(user=request.user, id=person_id).first()
        if person is None:
            return create_error_response('invalid_user')

        person.delete()

        return Response({
        }, status=status.HTTP_200_OK)


class persons(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        persons = get_persons(user=request.user)

        serializer = PersonSerializer(instance=persons, many=True)

        return Response({
            'persons': serializer.data,
            # @TODO: Remove when the next update is online
            'weeklyStats': {},
        }, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = PersonWriteSerializer(data=request.data)
        if serializer.is_valid():
            person = serializer.save(user=request.user, balance=0)

            return Response({
                'personId': person.id,
                'status': status.HTTP_200_OK,
            })
        else:
            return create_error_response(serializer.error_messages)


class person_transactions(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, person_id, format=None):
        person = Person.objects.filter(user=request.user, id=person_id).first()
        if person is None:
            return create_error_response('invalid_user')

        transactions = Transaction.objects.filter(
            person=person
        ).order_by('-date_added')

        serializer = TransactionReadSerializer(
            instance=transactions, many=True
        )

        return Response({
            'transactions': serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request, person_id, format=None):
        person = Person.objects.filter(user=request.user, id=person_id).first()
        if person is None:
            return create_error_response('invalid_user')

        serializer = TransactionWriteSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save(person=person)

            person.update_balance()

            return Response({
                'transactionId': transaction.id,
                'status': status.HTTP_200_OK,
            })
        else:
            return create_error_response(serializer.error_messages)


class person_scheduled_transactions(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, person_id, format=None):
        person = Person.objects.filter(user=request.user, id=person_id).first()
        if person is None:
            return create_error_response('invalid_user')

        transactions = ScheduledTransaction.objects.filter(
            person=person
        ).order_by('-date_added')

        serializer = ScheduledTransactionSerializer(
            instance=transactions, many=True
        )

        return Response({
            'transactions': serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request, person_id, format=None):
        person = Person.objects.filter(user=request.user, id=person_id).first()
        if person is None:
            return create_error_response('invalid_user')

        serializer = ScheduledTransactionWriteSerializer(data=request.data)
        if serializer.is_valid():
            scheduled_transaction = serializer.save(person=person)

            return Response({
                'scheduledTransactionId': scheduled_transaction.id,
                'status': status.HTTP_200_OK,
            })
        else:
            return create_error_response(serializer.error_messages)


class scheduled_transaction(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, transaction_id, format=None):
        transaction = ScheduledTransaction.objects.filter(
            person__user=request.user, id=transaction_id
        ).first()

        if transaction is None:
            return create_error_response('invalid_user')

        transaction.delete()

        return Response({
        }, status=status.HTTP_200_OK)


class transaction(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, transaction_id, format=None):
        transaction = Transaction.objects.filter(
            person__user=request.user, id=transaction_id
        ).first()

        if transaction is None:
            return create_error_response('invalid_user')

        person = transaction.person

        transaction.delete()

        person.update_balance()

        return Response({
        }, status=status.HTTP_200_OK)


class transactions(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        transactions = Transaction.objects.filter(
            person__user=request.user
        ).order_by('-date_added')

        serializer = TransactionReadSerializer(
            instance=transactions, many=True
        )

        return Response({
            'transactions': serializer.data,
        }, status=status.HTTP_200_OK)


def get_persons(**kwargs):
    filter_last_week = Q(
        transaction__date_added__gte=timezone.now()-timedelta(days=7)
    )

    return Person.objects.filter(
        **kwargs
    ).annotate(
        weekly_amount=Sum('transaction__amount', filter=filter_last_week),
        weekly_total=Count('transaction__amount', filter=filter_last_week)
    ).order_by('name')
