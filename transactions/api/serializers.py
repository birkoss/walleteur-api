from rest_framework import serializers

from ..models import Person, Transaction


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'balance']
