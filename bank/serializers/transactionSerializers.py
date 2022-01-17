from rest_framework import serializers
from bank.models import Transaction
from django.db.models import Sum

class TransactionSerializer(serializers.ModelSerializer): 
    
    def validate(self, data):
        """[Função responsável por validar]

        Args:
            data ([type]): [Data]

        Raises:
            serializers.ValidationError: [Limita os depósitos a 2000.]
            serializers.ValidationError: [Não deixa transferir ou depósitar valores negativos.]
            serializers.ValidationError: [Não deixa transferir ou depósitar valor igual a 0.]
            serializers.ValidationError: [Não deixa transferir se não possuir saldo.]

        Returns:
            [type]: [description]
        """
        if ( data["type_operation"].pk == 1 and data["value"] > data["type_operation"].max_value ):        
            raise serializers.ValidationError({"value": "Deposits greater than 2000 are not allowed"})
        if ( data["value"] < 0  ):        
            raise serializers.ValidationError({"value": "We do not accept negative values"})
        if ( data["value"] == 0  ):        
            raise serializers.ValidationError({"value": "the value must be greater than zero"})
        
        if ( data["type_operation"].pk == 2):
            total_deposit = Transaction.objects.filter(account_shipping = data["account_shipping"].pk, account_received = data["account_shipping"].pk, type_operation = 1 ).aggregate(Sum('value'))
            total_transfer = Transaction.objects.filter(account_shipping = data["account_shipping"].pk, type_operation = 2 ).aggregate(Sum('value'))
            
            if ( total_deposit["value__sum"] == None  ):
                total_deposit["value__sum"]  = 0
            if ( total_transfer["value__sum"] == None ):
                total_transfer["value__sum"] = 0
            
            saldo =  total_deposit["value__sum"] - total_transfer["value__sum"] 
            if( saldo < data["value"]  ): 
                raise serializers.ValidationError({"value": "you don't have enough balance"})
        return data
    
    class Meta:
        model = Transaction
        fields = "__all__"