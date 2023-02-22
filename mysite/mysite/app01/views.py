from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from django import forms
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


def show_users(request):
    if request.method == "GET":
        user_list = models.UserList.objects.all()
        return render(request, 'users.html', {"users": user_list})
    else:
        user_name = request.POST.get("name")
        password = request.POST.get("password")
        user_age = request.POST.get("age")
        phone_num = request.POST.get("phone_num")
        print(user_name, password, user_age, phone_num)

        models.UserList.objects.create(name=user_name, password=password, age=user_age, phone_number=phone_num)

        return redirect("/users/")


def delete_user(request):
    pk = request.GET.get("id")
    print(pk)
    models.UserList.objects.filter(id=pk).delete()

    return redirect("/users/")


def add_user(request):
    if request.method == "GET":
        department = models.Department.objects.all()
        return render(request, 'add_user.html', {"department": department})

    if request.method == "POST":
        user_name = request.POST.get("name")
        password = request.POST.get("password")
        user_age = request.POST.get("age")
        gender = request.POST.get("gender")
        salary = request.POSt.get("salary")
        create_time = request.POST.get("create_time")
        department = request.POST.get("department")
        phone_num = request.POST.get("phone_num")

        for info in request.POST:
            print(info)
        models.UserList.objects.create(name=user_name, password=password, age=user_age, phone_number=phone_num, gender=gender, salary=salary, create_time=create_time, department=department)
        print("成功添加用戶")
        return redirect('/users/')


class UserForm(forms.ModelForm):
    class Meta:
        model = models.UserList
        # fields = ["name", "password", "age"]
        # 也可以是使用 fileds = '__all__'
        fields = '__all__'
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"})
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            print(name, field)
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def add_user2(request):
    form = UserForm
    if request.method == "GET":
        return render(request, "add_user2.html", {"form": form})