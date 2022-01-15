from django.db import models
from django.contrib.auth.models import User, AbstractUser

class User(AbstractUser):
    cpf = models.BigIntegerField(blank=False, null=False)
    
class Account(models.Model):
    agency = models.IntegerField(blank=False, null=False)
    account = models.IntegerField()
    user = models.OneToOneField(
        User,  
        on_delete=models.CASCADE,
        primary_key=True,
    )    
    saldo =  models.DecimalField( max_digits = 6, decimal_places = 2)

class Operation(models.Model):
    type_operation = models.IntegerField()
    name_operation = models.CharField(max_length=30)
    max_value = models.DecimalField( max_digits = 6, decimal_places = 2)

class Transacoes(models.Model):
    valor = models.DecimalField( max_digits = 6, decimal_places = 2)
    account_shipping = models.ForeignKey(
        Account, 
        on_delete=models.CASCADE,
        related_name='account_shipping', 
    )
    account_received = models.ForeignKey(
        Account, 
        on_delete=models.CASCADE,
        related_name='account_received', 
    )
    type_operation = models.ForeignKey(
        Operation, 
        on_delete=models.CASCADE,
    )
    