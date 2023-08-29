from django.urls import path,include,re_path
from.views import *
app_name='Auth'

urlpatterns=[
    path('',signup),
    path('settings/',settings),
    path('logout/',logout,name='logout'),
    path('signin/',signin),
    path('save-notes/',save_notes, name='save_notes'),

]