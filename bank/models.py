from __future__ import annotations
from django.db import models
from django.contrib.auth.models import User, AbstractUser

class User(AbstractUser):
    username = None
    cpf = models.BigIntegerField(blank=False, null=False, unique=True)
    USERNAME_FIELD = 'cpf'
        
class Account(models.Model):
    agency = models.IntegerField(blank=False, null=False)
    account = models.IntegerField()
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )    
    saldo =  models.DecimalField( max_digits = 6, decimal_places = 2, default=0)

class Operation(models.Model):
    id = models.IntegerField(primary_key=True)
    name_operation = models.CharField(max_length=30)
    max_value = models.DecimalField( max_digits = 6, decimal_places = 2, null=True)

class Transaction(models.Model):
    value = models.DecimalField( max_digits = 6, decimal_places = 2)
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
    