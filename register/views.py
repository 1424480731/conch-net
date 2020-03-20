from django.shortcuts import render,redirect
from register.models import User
from django.http import JsonResponse,HttpResponse
import time
from conch.utils import write_image
# Create your views here.

def verify_user_exist(request):
    if request.method=="POST":
        username = request.POST.get('username')
        print(username,request.POST)
        if User.objects.filter(username=username):
            return JsonResponse({'data':1})
        return JsonResponse({'data':0})

def sign_in(request):
    if request.method=='POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        birthday = request.POST.get('birthday')
        id_number = request.POST.get('id_number')
        real_name = request.POST.get('real_name')
        habby = request.POST.get('habby')
        email = request.POST.get('email')
        img = request.FILES.get('photo')
        print(username,img)
        imag_path = './static/images/' + username + '_' + str(int(time.time())) + '.' + img.name.split('.')[-1]
        if img.name.split('.')[-1] not in ['jpeg','jpg','png']:
            return JsonResponse({'data':'请上传jpeg，jpg，png三种格式的图片'})
        write_image(img,imag_path)
        try:
            User.objects.create(username=username,password=password,phone_number=phone,birthday=birthday\
                            ,id_card_num=id_number,real_name=real_name,email=email,habby=habby,img=imag_path[1:])
            return render(request, '01_Home.html',{'user':None})
        except:
            return JsonResponse({'data':'用户信息上传失败'})
    return JsonResponse({'data':0})

