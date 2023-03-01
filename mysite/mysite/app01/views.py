from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
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


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名",
                               max_length=32,
                               widget=forms.TextInput(),
                               required=True
                               )
    password = forms.CharField(label="密码",
                               max_length=64,
                               widget=forms.PasswordInput(),
                               required=True
                               )

    def clean_password(self):
        print(self.cleaned_data.get("password"))
        pwd = encrypt.md5(self.cleaned_data.get("password"))
        return pwd


def login(request):
    """重构login模块，更新数据校验功能"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {"form": form})
    elif request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user_data = models.Admin.objects.get(**form.cleaned_data)
            if user_data:
                """
                1.验证成功跟以后网站生成随机字符串写入到cookie中
                2.然后再将随机字符串写入到session中
                3.request.session["info"] = {'id':user_data.id,'name':user_data.username} 使用该条语句进行存储
                """
                request.session["info"] = {'id':user_data.id, 'name':user_data.username}
                return redirect('/users/')
            else:
                form.add_error("password", "用户名或者密码错误")
        return render(request, 'login.html', {'form': form})


def logout(request):
    request.session.clear()
    return redirect('/login/')

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
        models.UserList.objects.create(name=user_name, password=password, age=user_age, phone_number=phone_num,
                                       gender=gender, salary=salary, create_time=create_time, department=department)
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
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def add_user2(request):
    if request.method == "GET":
        form = UserForm()
        return render(request, "add_user2.html", {"form": form})

    elif request.method == "POST":
        form = UserForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/users/')

        else:
            return render(request, 'add_user2.html', {"form": form})


def update_user2(request, pk):
    if request.method == "GET":
        fix_data = models.UserList.objects.get(id=pk)
        form = UserForm(instance=fix_data)
        return render(request, 'update_user2.html', {"form": form})
    else:
        fix_data2 = models.UserList.objects.get(id=pk)
        form = UserForm(request.POST, instance=fix_data2)
        if form.is_valid():
            form.save()
            return redirect('/users/')
        else:
            return render(request, 'update_user2.html', {"form": form})


def delete_user2(request, pk):
    if request.method == "GET":
        models.UserList.objects.get(id=pk).delete()

        return redirect('/users/')


# 靓号管理
def phone_list(request):
    if request.method == "GET":
        data_dict = {}
        res_content = request.GET.get("content")
        page_num = int(request.GET.get("page", 1))

        if res_content:
            data_dict["mobile__contains"] = res_content
        # 分页操作
        search_content = models.PhoneNumber.objects.filter(**data_dict)

        paginator = Paginator(search_content, 2)
        page_obj = paginator.get_page(page_num)

        return render(request, 'phone_list.html', {'page_obj': page_obj})


class NumberForm(forms.ModelForm):
    # 校验方式1
    # mobile = forms.CharField(
    #     label="电话号码",
    #     validators=[RegexValidator(r'/^13[0-9]\d{8}$/', '格式错误'), ],
    # )

    class Meta:
        model = models.PhoneNumber
        fields = '__all__'
        # exclude = ['level']
        # fields = ['mobile', 'level', 'status', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': name}

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        if models.PhoneNumber.objects.filter(mobile=txt_mobile):
            raise ValidationError("号码已经存在")
        else:
            return txt_mobile


def add_phone(request):
    if request.method == "GET":
        form = NumberForm()
        return render(request, 'add_phone.html', {'form': form})

    elif request.method == "POST":
        form = NumberForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/phone_list/")
        else:
            return render(request, 'add_phone.html', {'form': form})


class FixNumber(forms.ModelForm):
    mobile = forms.CharField(label="手机号码")

    class Meta:
        model = models.PhoneNumber
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': name}

    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        if models.PhoneNumber.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists():
            raise ValidationError("号码已经存在")
        return txt_mobile


def update_phone(request, pk):
    if request.method == "GET":
        phone_data = models.PhoneNumber.objects.get(id=pk)
        form = FixNumber(instance=phone_data)
        return render(request, 'update_phone.html', {'form': form})
    elif request.method == "POST":
        phone_data = models.PhoneNumber.objects.get(id=pk)
        form = FixNumber(request.POST, instance=phone_data)
        if form.is_valid():
            form.save()
            return redirect('/phone_list/')
        else:
            return render(request, 'update_phone.html', {'form':form})


def delete_phone(request, pk):
    if request.method == "GET":
        models.PhoneNumber.objects.get(id=pk).delete()
        redirect('/phone_list/')


def admin_list(request):
    queryset = models.Admin.objects.all()
    return render(request, 'admin_list.html', {"admin_list": queryset})


from .utils import encrypt
class AdminModelForm(forms.ModelForm):

    conform_password = forms.CharField(
        max_length=64,
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'conform_password']
        widgets = {
            'password': forms.PasswordInput
        }

    def clean_password(self):
        pwd = self.cleaned_data["password"]
        pwd = encrypt.md5(pwd)
        return pwd

    def clean_conform_password(self):
        cpwd = self.cleaned_data["conform_password"]
        cpwd = encrypt.md5(cpwd)
        pwd = self.cleaned_data["password"]
        if cpwd == pwd:
            return cpwd
        else:
            raise ValidationError("密码输入不一致，请确认密码")


def add_admin(request):
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, 'add_base.html', {'form': form})

    elif request.method == "POST":
        form = AdminModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin_list/')

        else:
            return render(request, 'add_base.html', {'form': form})


def update_admin(request, aid):
    if request.method == "GET":
        admin_info = models.Admin.objects.get(id=aid)
        form = AdminModelForm(instance=admin_info)
        return render(request, 'add_base.html', {"form": form})
    elif request.method == "POST":
        admin_info = models.Admin.objects.get(id=aid)
        form = AdminModelForm(instance=admin_info, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin_list/')
        else:
            return render(request, 'add_base.html', {"form": form})


class ResetPasswordForm(forms.ModelForm):

    flag = True

    conform_password = forms.CharField(
        label="确认密码",
        max_length=64,
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.Admin
        fields = ['password', 'conform_password']
        widgets = {
            "password": forms.PasswordInput
        }

    def clean_password(self):
        pwd = self.cleaned_data["password"]
        pwd = encrypt.md5(pwd)

        old_pwd = models.Admin.objects.filter(id=self.instance.pk, password=pwd).exists()
        print(old_pwd)
        if old_pwd:
            print('密码是旧密码')
            self.flag = False
            raise ValidationError("不能使用旧密码")
        return pwd

    def clean_conform_password(self):
        if not self.flag:
            self.flag = True
            return self.cleaned_data["conform_password"]
        print(self.cleaned_data)
        print(self.cleaned_data)
        print(self.cleaned_data)
        c_pwd = self.cleaned_data["conform_password"]
        c_pwd = encrypt.md5(c_pwd)
        pwd = self.cleaned_data["password"]
        if pwd != c_pwd:
            raise ValidationError('密码输入不一致，请重新输入！')
        else:
            return c_pwd



def reset_password(request, aid):
    if request.method == "GET":
        admin_info = models.Admin.objects.get(id=aid)
        form = ResetPasswordForm(instance=admin_info)
        return render(request, 'add_base.html', {'form': form, 'title': admin_info.username})
    elif request.method == "POST":
        admin_info = models.Admin.objects.get(id=aid)
        form = ResetPasswordForm(data=request.POST, instance=admin_info)
        if form.is_valid():
            form.save()
            return redirect('/admin_list/')
        else:
            return render(request, 'add_base.html', {'form': form})