from django.contrib import admin
from django.urls import path
from .api.user import UserAPI

urlpatterns = [
    path('users/', UserAPI.as_view()),
]
