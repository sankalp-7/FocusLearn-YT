from django.urls import path,include,re_path
from.views import *
app_name='Auth'

urlpatterns=[
    path('',signup),
    path('settings/',settings),
    path('signin/',signin),


]