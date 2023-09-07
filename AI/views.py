import textwrap
from django.shortcuts import render
from apiclient.discovery import build
from django.http import JsonResponse
import json
import re
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import urllib.request
import json
import urllib
import redis
from focus_yt.settings import redis_connection
import pprint
import time
# Create your views here.
openai.api_key = ""
api_key="AIzaSyCRzrt-0rHNQ4DzybpAeWSO_q7SyDR2OJo"
youtube=build('youtube','v3',developerKey=api_key)

def get_cached_transcript(video_id):
    cached_transcript = redis_connection.get(f'transcript:{video_id}')
    return cached_transcript
def cache_transcript(video_id, transcript_text):
    redis_connection.set(f'transcript:{video_id}', transcript_text)


def home(request):
    return render(request,'AI/home.html')

def get_videos(request):
    if request.method=='POST':
        yt_query=request.POST['query']
        req=youtube.search().list(q=yt_query,part='snippet',type='video',relevanceLanguage='en',maxResults=50)
        res=req.execute()
        return render(request, 'AI/main.html', {'video_data': res,'q':yt_query})
    return render(request,'AI/main.html')

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
            

        def split_text_into_chunks(text, max_chunk_size):
            return textwrap.wrap(text, max_chunk_size)
        max_chunk_size = 4000
        transcript_chunks = split_text_into_chunks(transcript_text, max_chunk_size)
        summaries = ""
        
        try:
            for chunk in transcript_chunks:
                response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{chunk}\n\nCreate short concise summary"}
                ],
                max_tokens=250,
                temperature=0.5
            )
            summaries += response['choices'][0]['message']['content'].strip() + " "
            return render(request, 'AI/summary.html', {'summary': summaries,'title_yt':req_title})
        except Exception as e:
            return JsonResponse({'error':e})
    return JsonResponse({'error': 'Invalid request.'})


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


        
