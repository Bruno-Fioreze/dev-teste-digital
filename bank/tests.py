from django.test import TestCase
from django.test import Client
from bank.models import User, Account
import unittest
import json
# Create your tests here.

class TestUserBank(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        
    def test_bank_return_400(self):
        url = "/users/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)
        
    def test_bank_return_200(self): 
        url = "/users/"
        data = {
            "cpf": "47949895802",
            "first_name": "Bruno",
            "last_name": "Fioreze"
        }
        response = self.client.post(url, data)
        data_return = response.content.decode("utf8")
        data_return = json.loads( data_return )
        user = User.objects.get(id=data_return["user"]["id"])
        user.delete()
        self.assertEqual(response.status_code, 200)
        
    def test_bank_return_400(self): 
        url = "/users/"
        data = {
            "cpf": "47949895803",
            "first_name": "Bruno",
            "last_name": "Fioreze"
        }
        response = self.client.post(url, data)
        data_return = response.content.decode("utf8")
        data_return = json.loads( data_return )
        user = User.objects.get(id=data_return["user"]["id"])
        response = self.client.post(url, data)
        user.delete()
        
        self.assertEqual(response.status_code, 400)
        
        
class TransactionBank(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        
    def test_transaction_bank_get_200(self):
        url = "/transaction/"
        data = {}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
    
    def test_transaction_bank_raise_exception(self):
        url = "/transaction/"
        parameters = (
            {"value": 50, "account_shipping": 1, "account_received": 1, "type_operation": None},
            {"value": 50, "account_shipping": 1, "account_received": None, "type_operation": 1},
            {"value": 50, "account_shipping": None, "account_received": 1, "type_operation": 1},
            {"value": None, "account_shipping": 1, "account_received": 1, "type_operation": 1},
        )
        with self.subTest(parameters=parameters):
            for parameter in parameters:
                self.assertRaises(Exception, self.client.post, url, parameter)
        
    def test_transaction_bank_negative_value(self):
        url = "/users/"
        data = {
            "cpf": "47949833999",
            "first_name": "Bruno",
            "last_name": "Fioreze"
        }
        response = self.client.post(url, data)
        data_return = response.content.decode("utf8")
        data_return = json.loads( data_return )
        
        user_shipping = User.objects.get(id=data_return["user"]["id"])
        account_shipping = Account.objects.get(user_id=user_shipping.pk)
        
        url = "/transaction/"
        data =  {"value": -2000, "account_shipping": account_shipping.pk, "account_received": account_shipping.pk, "type_operation": 1} 
        response = self.client.post(url, data)
        
        data_return = response.content.decode("utf8")
        data_return = json.loads( data_return )
        
        user_shipping.delete()
        account_shipping.delete()
        self.assertEqual(data_return["value"][0], "We do not accept negative values")
        self.assertEqual(response.status_code, 400)
        
     
    def test_transaction_bank_zero_value(self):
        url = "/users/"
        data = {
            "cpf": "31949895802",
            "first_name": "Bruno",
            "last_name": "Fioreze"
        }
        response = self.client.post(url, data)
        
        data_return = response.content.decode("utf8")

        data_return = json.loads( data_return )
        user_shipping = User.objects.get(id=data_return["user"]["id"])
        account_shipping = Account.objects.get(user_id=user_shipping.pk)
        
        url = "/transaction/"
        data =  {"value": 0, "account_shipping": account_shipping.pk, "account_received": account_shipping.pk, "type_operation": 1} 
        response = self.client.post(url, data)
        
        data_return = response.content.decode("utf8")
        data_return = json.loads( data_return )
        
        user_shipping.delete()
        account_shipping.delete()
        self.assertEqual(data_return["value"][0], "the value must be greater than zero")
        self.assertEqual(response.status_code, 400)
        
    def test_transaction_transfer_greater_than_balance(self):
        url = "/users/"
        data = {
            "cpf": "47949895999",
            "first_name": "Bruno",
            "last_name": "Fioreze"
        }
        response = self.client.post(url, data)
        data_return = response.content.decode("utf8")
        data_return = json.loads( data_return )
        user_shipping = User.objects.get(id=data_return["user"]["id"])
        account_shipping = Account.objects.get(user_id=user_shipping.pk)
        
        data = {
            "cpf": "47949895998",
            "first_name": "Bruno",
            "last_name": "Fioreze"
        }
        response = self.client.post(url, data)
        data_return = response.content.decode("utf8")
        data_return = json.loads( data_return )
        user_receveid = User.objects.get(id=data_return["user"]["id"])
        
        account_receveid = Account.objects.get(user_id=user_shipping.pk)
        
        url = "/transaction/"
        
        data =  {"value": 1900, "account_shipping": account_shipping.pk, "account_receveid": account_receveid.pk, "type_operation": 1} 
        response = self.client.post(url, data)
        
        data =  {"value": 3000, "account_shipping": account_shipping.pk, "account_received": account_receveid.pk, "type_operation": 2} 
        response = self.client.post(url, data)
        
        data_return = response.content.decode("utf8")
        data_return = json.loads( data_return )
        
        self.assertEqual(data_return["value"][0], "you don't have enough balance")
        
        user_shipping.delete()
        user_receveid.delete()
        
        account_shipping.delete()
        account_receveid.delete()
        self.assertEqual(response.status_code, 400)
        

class AccountBank(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        
    #n??o fiz os testes desse end-point, pois ele usa ferramentas do django,