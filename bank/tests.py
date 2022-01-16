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