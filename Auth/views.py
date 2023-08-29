from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from.models import UserProfile,Notes
from.forms import NotesForm

# Create your views here.
def signup(request):
    if request.method=='POST':
        username=request.POST['full_name']
        email=request.POST['email']
        password=request.POST['password']
        cpassword=request.POST['cpassword']

        if password==cpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('/')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('/')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                user_model=User.objects.get(username=username)
                new_profile=UserProfile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('/settings/')


        else:
            messages.info(request,'Password not matching')
            return redirect('/')
    return render(request,'Auth/signup.html')
def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/search/')
        else:
            messages.info(request,'Credentials Invalid')
            return redirect('/')
    return render(request,'Auth/signin.html')
@login_required(login_url='/signin')
def logout(request):
    auth.logout(request)
    return redirect('/signin/')
@login_required(login_url='/signin')
def settings(request):
    print("settings loading/......")
    curr_user=UserProfile.objects.get(user=request.user)
    if request.method=='POST':
        curr_user.leetcode_link=request.POST['leetcode']
        curr_user.github_link=request.POST['github']
        curr_user.codechef_link=request.POST['codechef']
        curr_user.save()
        return redirect('/search/')
    return render(request,'Auth/settings.html')

def save_notes(request):
    if request.method == 'POST' and request.is_ajax():
        form = NotesForm(request.POST)
        if form.is_valid():
            video_id = form.cleaned_data['video_id']
            notes = form.cleaned_data['content']
            user_profile = UserProfile.objects.get(user=request.user)
            Notes.objects.create(user_profile=user_profile, video_id=video_id, content=notes)
            return JsonResponse({'message': 'Notes saved successfully.'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid request.'}, status=400)