from django.urls import path,include,re_path
from.views import *
app_name='AI'

urlpatterns=[
    path('',home,name='home'),
    path('get-videos/',get_videos),
    path('summarize-view/',summarize_view),
    path('quiz-view/',quiz_view),

]