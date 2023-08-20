from django.shortcuts import render

# Create your views here.


def home(request):
    if request.method=='POST':
        yt_query=request.POST['query']
        print(yt_query)
        return render(request,'AI/home.html')
    return render(request,'AI/home.html')