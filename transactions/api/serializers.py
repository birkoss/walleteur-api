from rest_framework import serializers

from ..models import Person, ScheduledTransaction, Transaction


class PersonSerializer(serializers.ModelSerializer):
    weekly_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    weekly_total = serializers.IntegerField()

    class Meta:
        model = Person
        fields = ['id', 'name', 'balance', 'weekly_amount', 'weekly_total']


class TransactionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['reason', 'amount']


class ScheduledTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledTransaction
        fields = ['id', 'reason', 'amount', 'date_next_due',
                  'interval_amount', 'interval_type']


class ScheduledTransactionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledTransaction
        fields = ['reason', 'amount', 'date_next_due',
                  'interval_amount', 'interval_type']


class TransactionReadSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'reason', 'amount', 'person', 'date_added', 'type']
