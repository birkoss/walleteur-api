from rest_framework import serializers

from ..models import Person, ScheduledTransaction, Transaction


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'balance']


class TransactionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['reason', 'amount']


class ScheduledTransactionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledTransaction
        fields = ['reason', 'amount', 'date_next_due']


class TransactionReadSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'reason', 'amount', 'person', 'date_added']
