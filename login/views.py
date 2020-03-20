from django.shortcuts import render,redirect
from register.models import User
from django.http import HttpResponse,JsonResponse
# Create your views here.
def login(request):
    try:
        obj = redirect('mision:home')
        if request.method == 'POST':
            username =request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.get(username=username,password=password)
            if user:
                request.session['status']=1
                obj.set_cookie('username',username,max_age=60*60*24*7)
    except:
        pass
    return obj

def out(request):

    request.COOKIES.pop('username')
    request.session.pop('status')
    return redirect('mision:home')

