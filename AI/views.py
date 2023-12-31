import textwrap
from django.shortcuts import render
from apiclient.discovery import build
from django.http import JsonResponse
import json
import re
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import urllib.request
from django.contrib.auth.decorators import login_required
import json
import urllib
import redis
from focus_yt.settings import redis_connection
import pprint
import time

import time
#stops continuous api calls avoiding RateLimit errors
class RateLimiter:
    def __init__(self, request_interval):
        self.request_interval = request_interval
        self.last_request_time = time.time()
    def wait_for_ratelimit(self):
        current_time = time.time()
        print(current_time)
        elapsed_time = current_time - self.last_request_time
        print(elapsed_time)
        sleep_time = self.request_interval - elapsed_time
        if sleep_time > 0:
            print(f"stopping curr api req for {sleep_time} seconds")
            time.sleep(sleep_time)
        print("your good to go")
        self.last_request_time = time.time()
openai.api_key = ""
api_key=""
youtube=build('youtube','v3',developerKey=api_key)
def get_cached_transcript(video_id):
    cached_transcript = redis_connection.get(f'transcript:{video_id}')
    return cached_transcript
def cache_transcript(video_id, transcript_text):
    redis_connection.set(f'transcript:{video_id}', transcript_text)

@login_required(login_url='/signin/')
def home(request):
    return render(request,'AI/home.html')

@login_required(login_url='/signin/')
def get_videos(request):
    if request.method=='POST':
        yt_query=request.POST['query']
        req=youtube.search().list(q=yt_query,part='snippet',type='video',relevanceLanguage='en',topicId='/m/01k8wb',maxResults=50)
        res=req.execute()
        return render(request, 'AI/main.html', {'video_data': res,'q':yt_query})
    return render(request,'AI/main.html')

@login_required(login_url='/signin/')
def summarize_view(request):
    video_url = request.GET.get('url')
    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % video_url}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string
    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        # pprint.pprint(data)
        req_title=data['title']
        
    if video_url:
        #summarization logic using the video_url
        youtube_url="https://www.youtube.com/watch?v="+video_url
        match = re.search(r"v=([A-Za-z0-9_-]+)", youtube_url)
        if match:
            video_id = match.group(1)
        else:
            raise ValueError("Invalid YouTube URL")
        cached_transcript = get_cached_transcript(video_id)
        if cached_transcript:
            transcript_text = cached_transcript
            print("data coming from redis")
          
        else:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)

            transcript_text = ""
            for segment in transcript:
                transcript_text += segment["text"] + " "
            cache_transcript(video_id, transcript_text)

        summaries = ""
        
        try:
                response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"{transcript_text}\n\nCreate a summary, avoid any unimportant details."}
                    ],
                    max_tokens=200,
                    temperature=0.8
                )
        except:
                
                return JsonResponse({'error': 'ChatGPT May Be Down Pls Try Again Later...'})
                
        summaries += response['choices'][0]['message']['content'].strip() + " "
        return render(request, 'AI/summary.html', {'summary': summaries,'title_yt':req_title})
    return JsonResponse({'error': 'Invalid request.'})

@login_required(login_url='/signin/')
def quiz_view(request):
    video_url = request.GET.get('url')
    if video_url:
        youtube_url="https://www.youtube.com/watch?v="+video_url
        match = re.search(r"v=([A-Za-z0-9_-]+)", youtube_url)
        if match:
            video_id = match.group(1)
        else:
            raise ValueError("Invalid YouTube URL")
        cached_transcript = get_cached_transcript(video_id)
        if cached_transcript:
            transcript_text = cached_transcript
            print("quiz generating after redis cache stores yt transcript")
        else:
            print("not coming from here")
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = ""
            for segment in transcript:
                transcript_text += segment["text"] + " "
            cache_transcript(video_id, transcript_text)
        prompt='''Generate 10 quiz questions based on the text with multiple choices.create them in json format like:
{
 "questions":[
	{
	"question":"",
	"choices":[ ],
	"correct_choice":""
	}
	]
}
give result directly.'''
        try:
            rate_limiter = RateLimiter(request_interval=8)
            rate_limiter.wait_for_ratelimit()
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
            {"role": "system", "content": "You are a helpful assistant that generates questions."},
            {"role": "user", "content": transcript_text},
            {"role": "user", "content": prompt}
            ]
            )
            quiz_questions = response['choices'][0]['message']['content']
            print("Quiz Questions:")
            
            if type(quiz_questions)==list:
                quiz_questions=quiz_questions[0]
            return render(request,'AI/quiz.html',{'quiz_q':quiz_questions,'back':video_url})
        except:
            return JsonResponse({'error': 'Chatgpt error.Chatgpt May Be Down'})
    return JsonResponse({'error': 'Invalid request.'})

@login_required(login_url='/signin/')
def check_video_based_on_query(request):
        q=request.GET.get('query','') 
        video_url = request.GET.get('video_url') 
        if video_url:
            youtube_url="https://www.youtube.com/watch?v="+video_url
            match = re.search(r"v=([A-Za-z0-9_-]+)", youtube_url)
            if match:
                video_id = match.group(1)
            else:
                raise ValueError("Invalid YouTube URL")
        cached_transcript = get_cached_transcript(video_id)
        if cached_transcript:
            transcript_text = cached_transcript
        else:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = ""
            for segment in transcript:
                text = segment["text"]
                transcript_text += f"{text}\n"
            cache_transcript(video_id, transcript_text)
        prompt = f"Is there information about '{q}' in the video transcript:\n{transcript_text}\nAnswer:"
        
       
        try:
            print("trying chatgpt")
            rate_limiter = RateLimiter(request_interval=8)
            rate_limiter.wait_for_ratelimit()
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Is there information about '{q}' in the video transcript:\n{transcript_text}\n answer should be like:- Yes there is information about {q} in the video or No there is no such information about {q} in the video\nAnswer:"}
                ],
                max_tokens=50,
                temperature=0.5
                )
            time.sleep(5)
            answer = response['choices'][0]['message']['content'].strip() + " "
            return JsonResponse({'answer': answer})
        except Exception as e:
            return JsonResponse({'error': str(e)})


        
