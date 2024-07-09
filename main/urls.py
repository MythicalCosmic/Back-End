from django.urls import path, include
from .views import *

urlpatterns = [
    path('api-auth/login/', login_view, name='api-auth-login'),
    path('api-auth/logout/', logout_view, name='api-auth-logout'),
]