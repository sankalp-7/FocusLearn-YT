from django.urls import path,include
from.views import *
app_name='AI'

urlpatterns=[
    path('',home,name='home')
]