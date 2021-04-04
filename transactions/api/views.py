from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.utils import timezone

from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Person, Transaction

from core.helpers import create_error_response

from .serializers import PersonSerializer, TransactionWriteSerializer


class person(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

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

        return Response({
            'persons': serializer.data,
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

    def post(self, request, person_id, format=None):
        person = Person.objects.filter(user=request.user, id=person_id).first()
        if person is None:
            return create_error_response('invalid_user')

        serializer = TransactionWriteSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save(person=person)

            # Update person balance
            total_transactions = Transaction.objects.filter(
                person=person
            ).aggregate(Sum('amount'))
            newBalance = total_transactions['amount__sum']

            person.balance = newBalance
            person.save()

            return Response({
                'transactionId': transaction.id,
                'status': status.HTTP_200_OK,
            })
        else:
            print(serializer.error_messages)
            return create_error_response(serializer.error_messages)
