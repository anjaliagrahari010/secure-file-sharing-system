from django.urls import path
from .views import *
urlpatterns=[
    path('',home,name='home'),
    path('signup.html',signup,name='signup'),
    path('login.html',signin,name='login'),
]