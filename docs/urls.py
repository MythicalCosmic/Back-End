from django.urls import path
from .views import *

urlpatterns = [
    path('', docs, name="home")
]