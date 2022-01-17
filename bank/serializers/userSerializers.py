from rest_framework import serializers
from bank.models import User
from bank.serializers.dynamiciFelds import DynamicFieldsModelSerializer


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "cpf"]