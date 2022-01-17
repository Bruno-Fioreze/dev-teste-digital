from django.test import TestCase
from django.test import Client
from bank.models import User
import unittest
import json
# Create your tests here.

class TestBank(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        
    def test_bank_return_400(self):
        url = "/users/"
        data = {}
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
        user = User.objects.get(id=data_return["id"])
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
        user = User.objects.get(id=data_return["id"])
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
    
    def test_transaction_bank_get_search_200(self):
        url = "/transaction/?search=1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_transaction_bank_get_search_exception(self):
        url = "/transaction/?search="
        self.assertRaises(Exception, self.client.get, url)
    
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
        user_shipping = User.objects.get(id=data_return["id"])
        
        url = "/transaction/"
        data =  {"value": -2000, "account_shipping": data_return["id"], "account_received": data_return["id"], "type_operation": 1} 
        response = self.client.post(url, data)
        
        data_return = response.content.decode("utf8")
        data_return = json.loads( data_return )
        
        user_shipping.delete()
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
        
        user_shipping = User.objects.get(id=data_return["id"])
        url = "/transaction/"
        data =  {"value": 0, "account_shipping": user_shipping.pk, "account_received": user_shipping.pk, "type_operation": 1} 
        response = self.client.post(url, data)
        
        data_return = response.content.decode("utf8")
        data_return = json.loads( data_return )
        
        user_shipping.delete()
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
        user_shipping = User.objects.get(id=data_return["id"])
        
        data = {
            "cpf": "47949895998",
            "first_name": "Bruno",
            "last_name": "Fioreze"
        }
        response = self.client.post(url, data)
        data_return = response.content.decode("utf8")
        data_return = json.loads( data_return )
        user_receveid = User.objects.get(id=data_return["id"])
        
        url = "/transaction/"
        
        data =  {"value": 1900, "account_shipping": user_shipping.pk, "account_received": user_shipping.pk, "type_operation": 1} 
        response = self.client.post(url, data)
        
        data =  {"value": 3000, "account_shipping": user_shipping.pk, "account_received": user_receveid.pk, "type_operation": 2} 
        response = self.client.post(url, data)
        
        data_return = response.content.decode("utf8")
        data_return = json.loads( data_return )
        
        self.assertEqual(data_return["value"][0], "you don't have enough balance")
        
        user_shipping.delete()
        user_receveid.delete()
        self.assertEqual(response.status_code, 400)
        
