from datetime import timedelta

from django.db.models import Count, Sum
from django.utils import timezone

from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Person, Transaction

from core.helpers import create_error_response

from .serializers import (
    PersonSerializer, TransactionReadSerializer, TransactionWriteSerializer
)


class person(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, person_id, format=None):
        person = Person.objects.filter(user=request.user, id=person_id).first()
        if person is None:
            return create_error_response('invalid_user')

        serializer = PersonSerializer(instance=person)

        weekly_stats = []

        transactions = Transaction.objects.filter(
            person=person,
            date_added__gte=timezone.now()-timedelta(days=7)
        ).values('person__id').annotate(Sum('amount'), Count('amount'))
        for transaction in transactions:
            weekly_stats.append({
                'personId': transaction['person__id'],
                'amount': transaction['amount__sum'],
                'total': transaction['amount__count'],
            })

        return Response({
            'person': serializer.data,
            'weeklyStats': weekly_stats,
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
        persons = Person.objects.filter(user=request.user)

        serializer = PersonSerializer(instance=persons, many=True)

        weekly_stats = []

        transactions = Transaction.objects.filter(
            person__user=request.user,
            date_added__gte=timezone.now()-timedelta(days=7)
        ).values('person__id').annotate(Sum('amount'), Count('amount'))
        for transaction in transactions:
            weekly_stats.append({
                'personId': transaction['person__id'],
                'amount': transaction['amount__sum'],
                'total': transaction['amount__count'],
            })

        return Response({
            'persons': serializer.data,
            'weeklyStats': weekly_stats,
        }, status=status.HTTP_200_OK)

    def post(self, request, format=None):

        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            person = serializer.save(user=request.user, balance=0)

            return Response({
                'personId': person.id,
                'status': status.HTTP_200_OK,
            })
        else:
            print(serializer.error_messages)
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
            print(serializer.error_messages)
            return create_error_response(serializer.error_messages)


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
