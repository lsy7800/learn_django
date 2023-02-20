from django.shortcuts import render, HttpResponse
import requests


# Create your views here.


def index(request):
    return HttpResponse('欢迎打开app01')


def user_list(request):
    return render(request, 'user_list.html')


def show_template(request):
    name = 'lys'
    chor = ['lsy', '345', '888']
    chor_info = {"name": 'lsy', "age": 18, "gender": 1}
    return render(request, 'user_list.html', {'n1': name, 'n2': chor, 'n3': chor_info})


def unicom_new(request):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    res = requests.get("http://www.chinaunicom.com.cn/api/article/NewsByIndex/2/2022/11/news", headers=headers)
    data_list = res.json()
    print(data_list)
    return render(request, 'news.html', {'news': data_list})


def net_request(request):
    if request.method == "GET":
        print(request.GET)
        print(request.GET.get('title'))
        return HttpResponse("GET请求" + request.GET.get('title'))
    if request.method == "POST":
        print(request.POST)
        return HttpResponse("POST请求")


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        if username == 'lsy' and password == "123":
            return HttpResponse("登录成功")
        else:
            errMsg = "用户名或密码错误请重新输入"
            return render(request, 'login.html', {'errMsg': errMsg})
