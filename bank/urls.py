from django.contrib import admin
from django.urls import path
from .api.user import UserAPI
from .api.transaction import TransictionAPI
from .api.account import AccountBalanceAPI

urlpatterns = [
    path('users/', UserAPI.as_view()), 
    path('transaction/', TransictionAPI.as_view()),
    path('account/balance/', AccountBalanceAPI.as_view()),
]
