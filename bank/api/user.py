#django imports
from bank.serializers.userSerializers import UserSerializer
from bank.models import User, Account
from django.db import transaction


#lib imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as StatusCode

#my imports
from bank.utils.account import AccountUtils

class UserAPI(APIView): 
    
    queryset = User
    serializer_class = UserSerializer
    
    def get(self, request, format=None):
        """[Função responsável por listar os usuários]

        Args:
            request ([type]): [Data]

        Returns:
            [JSON]: [Retorna uma lista de usuários.]
        """
        users = self.queryset.objects.values("id","first_name", "last_name", "cpf").all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None): 
        """[Função responsável por cadastrar o usuário e criar a sua conta.]

        Args:
            request ([type]): [description]

        Returns:
            [JSON]: [Retorna o erro ou os dados.]
        """
        serializer = self.serializer_class(data=request.data)
        status_code = StatusCode.HTTP_200_OK
        
        if serializer.is_valid():
            with transaction.atomic():
                try:
                    user = serializer.save()
                    pk_account = AccountUtils.create_new_account( user )
                    message_or_data  = {"user": serializer.data, "pk_account": pk_account }
                except Exception as e:
                    transaction.set_rollback(True) 
                    status_code, message_or_data = ( StatusCode.HTTP_424_FAILED_DEPENDENCY, "Failed Dependency")
                return Response(data=message_or_data, status=status_code)
        return Response(serializer.errors, status=StatusCode.HTTP_400_BAD_REQUEST)