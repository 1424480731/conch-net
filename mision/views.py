from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from conch.mongo import MongoChengJiApi
from conch.utils import split_list
# Create your views here.
mcja = MongoChengJiApi()
def home(request):

    status = request.session.get('status')
    if status:
        username = request.COOKIES.get('username')
        print(request.COOKIES)
        return render(request, '01_Home.html', {'user': username})
    return render(request,'01_Home.html',{'user':None})

def search(request):
    page_num = 0
    search = request.POST.get('search')
    print(search)
    if search:
        request.session['cond']= search
        cond = {'cond':search}
        ret_list = split_list(mcja.get_fy_by_cond(cond),7)
        page_num = len(ret_list)
    else:
        request.session['cond'] = '全国'
        cond = {'cond':'全国'}
        ret_list = split_list(mcja.upToDateRent(cond),7)
        page_num=3

    if request.session.get('status',None) == 1:
        username = request.COOKIES.get('username')
        return render(request,'09_Properties_Grid_Map_Hover.html',{'user':username,'page_num':[i+1 for i in range(page_num)],'fy_list':ret_list[0]})
    return render(request,'09_Properties_Grid_Map_Hover.html',{'user':None,'page_num':[i+1 for i in range(page_num)],'fy_list':ret_list[0]})


def upToDateRent(request):
    cond_content = request.GET.get('cond').replace('\n','').replace(' ','')
    cond = {'cond':cond_content}
    ret_html = mcja.upToDateRent(cond)
    ret_dic = {}
    ret_dic.update(cond)
    ret_dic.update({'html_box':ret_html})
    return JsonResponse(ret_dic)


def page(request):

    index = int(request.GET.get('page'))-1
    cond_content = request.session.get('cond')
    cond = {'cond':cond_content}

    if cond_content=="全国":
        ret_list = split_list(mcja.upToDateRent(cond),7)
    elif '/' in cond_content:
        params = cond_content.split('/')
        print(params)
        road = params[0]
        start_price = params[1]
        end_price = params[2]
        cond = {'cond': road, 'start_price': start_price, 'end_price': end_price}
        request.session['cond'] = cond_content
        ret_list = split_list(mcja.get_road_list_by_price(cond), 7)
    else:
        ret_list = split_list(mcja.get_fy_by_cond(cond),7)


    return render(request, 'list_page_ajax.html',{'fy_list': ret_list[index]})


def location(request):

    cond_content = request.GET.get('area')
    cond = {'cond':cond_content}
    ret_list = mcja.get_location(cond)
    return JsonResponse({'data':ret_list})


def road(request):

    params=request.GET.get('cond').split('/')
    cond_content=params[0]
    start_price = params[1]
    end_price = params[2]

    cond = {'cond':cond_content,'start_price':start_price,'end_price':end_price}
    request.session['cond'] = request.GET.get('cond')
    ret_list = split_list(mcja.get_road_list_by_price(cond), 7)
    page_num = len(ret_list)
    if request.session.get('status', None) == 1:
        username = request.COOKIES.get('username')
        return render(request, '09_Properties_Grid_Map_Hover.html',{'user': username, 'page_num': [i + 1 for i in range(page_num)], 'fy_list': ret_list[0]})
    return render(request, '09_Properties_Grid_Map_Hover.html',{'user': None, 'page_num': [i + 1 for i in range(page_num)], 'fy_list': ret_list[0]})


def view_fy(request,id):
    status = request.session.get('status')
    cond_content = request.session.get('cond')
    if '/' in cond_content:
        params = cond_content.split('/')
        cond = {'cond':params[0],'id':id}
    else:
        cond = {'cond': cond_content,'id':id}
    fy = mcja.find_fy_by_id(cond)
    if status:
        username = request.COOKIES.get('username')
        print(request.COOKIES)
        return render(request, '11_Single_Properties_Standart.html', {'user': username,'fy':fy})
    return render(request,'11_Single_Properties_Standart.html',{'user':None,'fy':fy})
