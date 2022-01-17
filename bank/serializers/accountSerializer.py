from rest_framework import serializers
from bank.models import Transaction
from bank.serializers.dynamiciFelds import DynamicFieldsModelSerializer


class AccountBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__" 