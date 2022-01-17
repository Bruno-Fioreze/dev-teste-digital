#django imports
from bank.serializers.accountSerializer import AccountBalanceSerializer
from bank.models import Transaction, User, Account
from django.db.models import Sum
from django.shortcuts import get_object_or_404

#lib imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as StatusCode

#my imports

class AccountBalanceAPI(APIView):  
    queryset = Transaction 
    serializer_class = AccountBalanceSerializer
    
    def get(self, request):
        
        cpf = request.GET.get("cpf")
        user = get_object_or_404(User, cpf=cpf)
        account = get_object_or_404(Account, user_id=user.pk)
        
        total_deposit = Transaction.objects.filter(account_shipping = account.pk, type_operation = 1 ).aggregate(Sum('value'))
        total_transfer = Transaction.objects.filter(account_shipping = account.pk, type_operation = 2 ).aggregate(Sum('value'))
            
        if ( total_deposit["value__sum"] == None  ):
                total_deposit["value__sum"]  = 0
        if ( total_transfer["value__sum"] == None ):
                total_transfer["value__sum"] = 0
            
        balance =  total_deposit["value__sum"] - total_transfer["value__sum"] 
        return Response(  {"balance": balance}, 200 )