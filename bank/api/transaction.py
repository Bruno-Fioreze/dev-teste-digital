#django imports
from bank.serializers.transactionSerializers import TransactionSerializer
from bank.models import Transaction

#lib imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as StatusCode

#my imports

class TransictionAPI(APIView): 
    queryset = Transaction 
    serializer_class = TransactionSerializer
    
    def get(self, request, format=None): 
        """[Função responsável por listar as transações.]

        Args:
            request ([type]): [Data]

        Returns:
            [JSON]: [Retorna um json com uma lista de transações.]
        """
        users = self.queryset.objects.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None): 
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid() : 
            serializer.save()
            return Response(
                serializer.data, status=StatusCode.HTTP_200_OK
            )
        return Response(serializer.errors, status=StatusCode.HTTP_400_BAD_REQUEST)