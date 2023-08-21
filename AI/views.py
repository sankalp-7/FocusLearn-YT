from django.shortcuts import render
from apiclient.discovery import build
from django.http import JsonResponse
import json
import re
from youtube_transcript_api import YouTubeTranscriptApi
import torch
import torchaudio
import openai
import textwrap
from transformers import pipeline
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
        return render(request, 'AI/main.html', {'video_data': res,'q':yt_query})
    return render(request,'AI/main.html')

def summarize_view(request):
    video_url = request.GET.get('url')
    if video_url:
        #summarization logic using the video_url
        youtube_url="https://www.youtube.com/watch?v="+video_url
        match = re.search(r"v=([A-Za-z0-9_-]+)", youtube_url)
        if match:
            video_id = match.group(1)
        else:
            raise ValueError("Invalid YouTube URL")

        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        transcript_text = ""
        for segment in transcript:
            transcript_text += segment["text"] + " "
        def split_text_into_chunks(text, max_chunk_size):
            return textwrap.wrap(text, max_chunk_size)
        max_chunk_size = 4000

        transcript_chunks = split_text_into_chunks(transcript_text, max_chunk_size)
        summaries = ""
        openai.api_key = "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"
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
        print(summaries)

        # Render your template with the summary
        return render(request, 'AI/summary.html', {'summary': summaries})

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

        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ""
        for segment in transcript:
            transcript_text += segment["text"] + " "
        openai.api_key = "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"
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
        {"role": "system", "content": "You are a helpful assistant that generates questions."},
        {"role": "user", "content": transcript_text},
        {"role": "user", "content": "Generate 10 quiz questions based on the text with multiple choices.Avoid questions which are too easy or are irrelevant.Avoid questions which require a picture to solve them.create them in json format.json fields should be question,choices,correct_choice(this field contains the actual answer).Give answer directly"},
        ]
        )
        quiz_questions = response['choices'][0]['message']['content']
        print("Quiz Questions:")
        print(quiz_questions)
        return render(request,'AI/quiz.html',{'quiz_q':quiz_questions})
    return JsonResponse({'error': 'Invalid request.'})

