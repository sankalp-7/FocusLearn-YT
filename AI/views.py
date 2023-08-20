from django.shortcuts import render
from apiclient.discovery import build
from django.http import JsonResponse
import json
# Create your views here.

api_key="AIzaSyCRzrt-0rHNQ4DzybpAeWSO_q7SyDR2OJo"
youtube=build('youtube','v3',developerKey=api_key)
def home(request):
    return render(request,'AI/home.html')

def get_videos(request):
    if request.method=='POST':
        yt_query=request.POST['query']
        req=youtube.search().list(q=yt_query,part='snippet',type='video')
        res=req.execute()
        return render(request, 'AI/main.html', {'video_data': res})
    return render(request,'AI/main.html')
