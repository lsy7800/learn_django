# Django

## 安装Django

```python
pip install django # 默认安装最新版本的django
pip install django=="[version]" # 安装指定版本的django
```

## 创建项目

```python
django-admin startproject mysite
```

## 项目结构

```
│ manage.py  # 项目管理
└─mysite
        asgi.py        # 接收网络请求 异步
        settings.py    # 项目配置文件
        urls.py        # 路由
        wsgi.py        # 接收网络请求 同步
        __init__.py
```

## 应用(APP)

### 创建应用

```python
# ./mysite
python manage.py startapp app01
```

### APP文件

```
├─app01
│  │  admin.py  # 后台admin
│  │  apps.py   # app启动类
│  │  models.py # 操作数据库
│  │  tests.py	# 单元测试
│  │  views.py
│  │  __init__.py
│  │
│  └─migrations # 数据库字段变更
│          __init__.py
```

### 注册APP

创建应用后必须经过注册才能够使用

```python
# mysite/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 自己创建的应用需要注册收才能使用
    'app01.apps.App01Config',  # 注册应用
]
```

### 配置路由

```python
# mysite/urls.py
from app01 import views # 导入视图模块
urlpatterns = [
    path('index', views.index),
]
```

### 视图函数

```python
# mysite/app01.views.py
from django.shortcuts import render, HttpResponse
def index(request): # 视图函数需要默认参数request
    return HttpResponse("欢迎来到app01")
```

#### 静态模板

```python
# mysite/app01.views.py
from django.shortcuts import render, HttpResponse
# 去app目录下的templates目录寻找user_list.html (根据app的注册顺序，逐一去他们的templates目录中寻找)
# 如果优先在项目的根目录中寻找则需要在settings中将templates路径加入[os.path.join(BASEDIR, template)]
def user_list(request): # 视图函数需要默认参数request
    return render(request, 'user_list.html') # 第一个参数必须是request， 第二个参数为模板名称
```

```python
# 静态模板需要在app01中新建templates文件
# 新建user_list.html文件
```

#### 静态文件

在开发过程中一般将：

* CSS
* 图片
* JS

当做静态文件处理

```html
# 在app01下新建static文件夹
# 然后存入静态资源
<img src="/static/img/01.png" alt="err!"></img>

{% load static %}
<img src="{static '/img/01.png'}">
<link href="{% static '/plugins/bootstrap/css/bootstrap.min.css' %}"> # 注意前面的'/'在4.1.7中如果没有不会正确加载
<script src="{% static '/plugins/bootstrap/js/bootstrap,min.js' %}"></script>
```

#### 模板语法

模板语法的本质就是占位符

```python
# mysite/app01/views.py

def template(request):
    name = 'lsy'
    name_list = ['lsy', 'leb', 'wdl', 'lsz']
    name_infor = {"name": "lsy", "gender": 0, "age":28}
    return render(request, "user_list.html", {'n1': name, 'n2':name_list, 'n3': name_info}) # 将name命名为n1
```

```html
-- 单条数据
<h1>
    {{n1}}
</h1>

-- 多条数据
<h1>
    {% for name in n2 %}
    	{{name}}
    {% endfor %}
</h1>

-- 字典数据
<h1>
    {% for item in n3.keys %}
    	{{item}} # 输出key
    {% endfor %}
    
    {% for item in n3.values %}
    	{{item}} # 输出value
    {% endfor %}
    
    {% for item in n3.items %}
    	{{item}} # 输出(key:value)
    {% endfor %}
    
    {% for k, v in n3.items %}
    	{{k}}--{{v}} # 输出key-value
    {% endfor %}
</h1>

<!-- 条件语句 -->
{% if n==1 %}
	{{n1}}
{% elif n==2 %}
	{{n2}}
{% else %}
	{{n3}}
{% enif %}

```



### 启动程序

```python
# ./mysite
python manage.py runserver 127.0.0.1:8000
```

### 请求和响应

```python
# views.py
def ege(request):
    # request是一个对象，封装了用户通过浏览器发送过来的请求
    # 通过获取request的请求方式可以进行不同的操作
    if request.method == "GET":
        print(request.GET)
    	return HttpResponse("GET请求")
    if request.method == "POST":
        print (request.POST)
        return HttpResponse("POST请求")
    
    # 如果需要重定向使用 return redirect('https://www.baidu.com')
```

### 数据库操作

django在内部提供了ORM框架

ORM可以帮助我们创建，修改，删除数据库中的表，不需要写sql语句，但是无法创建数据库

#### 创建数据库

```sql
# 创建数据库
create database test DEFAULT CHARSET utf8 COLLATE utf9_general_ci;
```

#### 连接数据库

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # 数据库引擎
        'NAME': '[database-name]', # 数据库名称
        'USER': 'root', # 用户
        'PASSWORD': 'lsy930825', # 数据库密码
        'HOST': '127.0.0.1', # 地址
        'PORT': 3306, # 端口
    }
}
```

#### django操作表

* 创建表

* 删除表

* 修改表

  ```python
  # models.py
  from django.db import models
  class UserInfo(models.Model):
      name = models.CharFiled(max_length=32)
      password = models.charFiled(max_length=64)
      age = models.InterFiled()
  
      """
      create table app01_userinfo(
      	id bigint auto_increment primary key,
      	name varchar(32),
      	age int
      ) default charset=utf8;
      """
  ```

  ```python
  # 执行命令
  python manage.py makemigrarions
  python manage.py migrate
  ```

  删除和修改表只需要修改models中的对应模型即可

  在新增列时，由于可能存在数据，所以新增列必须要要指定新增列对应的数据：

  * 手动输入一个值

  * 设置默认值

    ```python
    age = models.IntegerFiled(default=2)
    ```

  * 允许为空

    ```python
    data = models.IntegerFiled(null=True, blank=True)
    ```


#### 操作表中的数据

* 新增数据

```python
# models.py 
class Department(models.Model):
    title = models.CharField(max_length=16)
    
Department.objects.create(title="销售部") # 在title中新增一行数据
"""
如果又多项数据，则需要create(title="abc", age="123")
"""
```

* 删除数据

```python
# models.py
class UserInfo(models.Model):
    name = models.CharField(max_length=16)
    password = models.CharField(max_length=64)
    age = models.IntegerField(null=True)
    
UserInfo.objects.filter(id=3).delete() # 删除id=3的数据
UserInfo.objects.all().delete() # 清空数据库所有数据
```

* 获取数据

```python
UserInfo.objects.all() # 获取所有数据
"""
获取到的数据类型为Queryset[type 为 list]
"""

UserInfo.objects.filter(id=1) # 过滤id=1的数据，数据类型依然为QuerySet
UserInfo.objects.filter(id=1).first() # 使用first()直接获取到对象不需要再对QuerySet进行遍历

UserInfo.objects.get(id=1) # 获取id=1的数据
```

* 更新数据

```python
UserInfo.objects.filter(id=1).update(password=9999) # 将id=1的数据更新为9999
UserInfo.objects.all().update(password=99999) # 将所有password修改为99999
```



#### 案例：用户管理

1.展示用户列表

* url
* 函数
  * 获取所有用户信息
  * HTML渲染

2.添加用户信息

* url
* 函数
  * GET请求
  * POST请求

编写数据模型

```python
# models.py
class Department(models.Model):
    """部门列表"""
    title = models.CharField(verbose_name="部门名称", max_length=64)
    
    def __str__:
        return self.title


class UserList(models.Model):
    """员工列表"""
    name = models.CharField(verbose_name='用户名', max_length=64)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    # 性别
    gender_choice = (
        (1, "男"),
        (2, "女")
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choice, default=1)
    phone_number = models.CharField(verbose_name="电话", max_length=11)
    salary = models.DecimalField(verbose_name="薪资", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name="入职时间", null=True, blank=True)
    # to 表示与哪张表进行关联
    # to_fields 表示与表中的哪一列数据进行关联
    # on_delete=models.CASCADE 表示级联删除，删除部门后与之关联的表信息均会删除
    # on_delete=models.SET_NULL 表示删除部门后与之关联的信息会设置为空
    department = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
```

对数据库进行迁移

```python
python manage.py makemigrations
python manage.py migrate
```

编写视图函数

```python
# views.py
def user_list(request):
    if request.method == "GET":
        # 请求数据
        user_list = models.User.objects.all()
        for user in user_list:
            print(user.gender) # 得到的结果是 1 或 2
            print(user.get_gender_display()) # 得到的结果是 男 或 女
            print(user.department_id) # 得到的是数据库中存储的部门id
            print(user.department) # 会进行自动连表查找获得id所对应的对象
            print(user.department.title) # 会连表获取该条数据title所对应的内容
            
        retrun render(request, 'users.html', {"users": user_list})
    if request.method == "POST":
        # 添加数据
        user_name = request.POST.get("name")
        password = request.POST.get("password")
        user_age = request.POST.get("age")
        phone_num = request.POST.get("phone_num")
        print(user_name, password, user_age, phone_num)
        models.UserList.objects.create(name=user_name, password=password, age=user_age, phone_number=phone_num)
        return redirect("/users/")
    
def add_user(request):
    # 添加数据
    if request.method == "GET":
        depart = models.Department.objetcs.all()
        return render(request, 'add_user.html', {"depart": depart})
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
    
def user_delete(request):
    # 删除数据
    pk = request.GET.get("id")
    print(pk)
    models.UserList.objects.filter(id=pk).delete()

    return redirect("/users/")

def user_fix(request):
    # 修改数据
    if request.method = "GET":
        pk = request.GET.get("id")
        print(pk)
        user_info = models.UserList.objects.filter(id=pk)
        return render(request, "user_fix.html", {"user_info":user_info})
    if request.method = "POST":
        pk = request.POST.get("id")
        user_name = request.POST.get("name")
        password = request.POST.get("password")
        user_age = request.POST.get("age")
        gender = request.POST.get("gender")
        salary = request.POSt.get("salary")
        create_time = request.POST.get("create_time")
        department = request.POST.get("department")
        phone_num = request.POST.get("phone_num")
        
        models.UserList.objects.filter(id=pk).update(name=user_name, password=password, age=user_age, gender=gender, salary=salary, create_time=create_time, department=department, phone_number=phone_num)
        print("数据修改成功")
    	retrun redirect("/users/")
```

编写路由

```python
# urls.py

urlpatterns = [
    path("users/", views.user_list),
    path("user_delete/", views.user_delete),
    path("user_add/", views.user_add),
    path("user_fix/", views.user_fix)
]
```

```html
<!-- users.html -->
<!-- 员工界面 -->
	<h1>用户列表</h1>
	<table class="table table-dark">
		<thead>
		<tr>
			<th>姓名</th>
			<th>密码</th>
			<th>年龄</th>
			<th>性别</th>
			<th>电话</th>
			<th>薪资</th>
			<th>入职</th>
			<th>部门</th>
			<th>操作</th>
		</tr>
		</thead>
		{% for user in users %}
		<tr>
			<td>{{user.name}}</td>
			<td>{{user.password}}</td>
			<td>{{user.age}}</td>
			<td>{{user.gender}}</td>
			<td>{{user.phone_number}}</td>
			<td>{{user.salary}}</td>
             <!-- 模板字符串需要进行格式化处理 -->
			<td>{{user.create_time | date:"Y-m-d"}}</td> 
			<td>{{user.department.title}}</td>
			<td><a href="/delete_info/?id={{user.id}}">删除数据</a></td>
		</tr>
		{% endfor %}
	</table>
```

### 模板继承

```html
<!-- 母板base.html -->
{% block content %}{% block %}

<!-- 子模板componts.html -->
<!-- 继承母板 -->
{% extends 'base.html' %}

<!-- 编辑内容 -->
{% block content %}
	<!-- content -->
{% end block %}
```

### Form和ModelForm

在新建用户时会遇到如下问题：

```
- 用户提交数据需要校验
- 页面应该存在错误提示
- 页面上的每一个字段都需要写入
- 关联的数据需要手动获取并循环展示在页面中
```

#### Form

```python
# views.py

class MyForm(Form):
    """通过类来定义form"""
    user = form.CharField(widget=forms.Input)
    pwd = form.CharField(widget=forms.Input)
    emmail = form.CharField(widget=forms.Input)

def user_add(request):
    if request.method == "GET":
        form = MyForm()
        return render(request, "add_user.html", {"form":form})
```

```html
<!-- add_user.html -->
<form>
    {{ form.user }}
    {{ form.pwd }}
    {{ form.email }}
</form>

<!-- 可以使用循环 -->
<form>
    {% for field in form %}
    	{{field}}
    {% endfor %}
</form>
```

#### ModelForm

```python
class MyForm(ModelForm):
    class Meta:
        model = UserList
        fields = ["name", "password", "age", "gender", "phone_number", "salary", "department"]
        # 如果需要一次性添加所有字段
        # fields = '__all__'
        
        # 使用插件为每个字段添加class属性
        widgets = {
            "name":forms.InputText({"class": "form-control"})
        }
        
        # 如果需要校验更详细的数据，需要对该字段单独进行限制
        name = forms.CharField(min_length=3)
        password = forms.CharField(label="密码", validators="[re]")
        # fields = [..., "name"]
        
    # 如果需要为所有的字段添加class属性
    def __init__(self, *args, **kwargs):
        # super()用来调用父类的方法
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-contorl", "placehoder": name}
        
def add_user(request):
    if request.method =="GET":
        form = MyForm()
        return render(request, 'add_user.html', {'form':form})
    elif request.method == "POST":
        form = MyForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/users/')
        else:
            return render(request, 'add_user.html', {'form':form})
            print(form.errors)
        
```

```html
<!-- add_user.html -->
{% form item in form %}
<label>{{item.label}}</label>
{{item}}
<!-- 如果需要显示错误信息 -->
{{form.errors.0}}
{% endfor %}
```

#### 编辑用户

* 点击编辑，跳转到编辑页面，携带ID
* 编辑页面（默认数据根据ID获取设置到页面中）
* 提交：
  * 错误提示
  * 数据校验
  * 更新数据

```python
# urls.py
urlspatterns = [
    path("<int>:pk/update_user/", views.update_user),
    path("<int>:pk/delete_user/", views.delete_user)
]
```



```python
# views.py

def update_user(request, pk):
    # 修改数据
    if requst.method == "GET":
        # 注意：使用get直接得到对象中的第一条数据
        update_user = models.User.objects.get(id=pk)
        # 注意：使用filter得到的是一个对象
        # update_user = models.User.objects.filter(id=pk).first()
        form = Myform(instance=update_user)
        return render(request, 'update_user.html', {"form": form})
    elif request.method == "POST":
        update_user = models.User.objects.get(id=pk)
        form = MyForm(data=request.POST, instance=update_user)
        if form.isvalid():
            form.save()
            return redirect('/users/')
        else:
            return render(request, 'update_user.html', {"form": form})

def delete_user(request, pk):
    # 删除数据
    if request.method == "GET":
        models.User.objects.get(id=pk).delete()
```

#### 时间组件



### 靓号管理

数据库表结构

* id
* mobile
* level(1-5)
* status(是否售卖)
* price

```python
# models.py
class PhoneNumber(models.Model):
    """定义一个靓号数据库"""
    mobile = models.CharField(max_length=11, verbose_name="手机号")

    lv_choice = (
        (1, "一级"),
        (2, "二级"),
        (3, "三级"),
        (4, "四级"),
        (5, "五级")
    )

    level = models.SmallIntegerField(choices=lv_choice, default=1, verbose_name="等级")

    status_choices = (
        (1, "以售卖"),
        (2, "待售卖")
    )

    status = models.SmallIntegerField(choices=status_choices, default=2, verbose_name="状态")
    price = models.IntegerField(default=99, verbose_name="价格")

    def __str__(self):
        return self.mobile
<<<<<<< HEAD
```



#### 功能（1）- 靓号列表

* URL
* 函数
  * 获取所有靓号
  * id 号码 价格 级别 状态

```python
# views.py
def phone_list(request):
    if request.method == "GET":
        phone_numbers = models.PhoneNumber.objects.all().order_by('-level')
        # 这里的order_by是用来进行排序的
        return render(request, 'phone_list.html', {"phone_numbers": phone_numbers})
```

```python
# urls.py
urlpatterns = [
    path('phone_list/', views.phone_list)
]
```

#### 功能（2）- 新建靓号

创建form类

```python
from django import forms
```



```python
# views.py
from django.core.validators import RegexValidator
class NumberForm(forms.ModelForm):
    # 校验手机号方式1
    mobile = forms.CharField(
    	label = "手机号",
        validators = [RegexValidator(r'/^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$/'，'手机格式错误')]
    )
    class Meta:
        model = models.PhoneNumber
        fields = '__all__'
        # 如果需要排除某个字段
        # exclude = ['level']
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': name}
    # 校验手机号方式2
	def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        res_info = models.PhoneNumber.objects.filter(mobile=txt_mobile).exists()
        if len(txt_mobile) != 11:
            raise ValidationError("格式错误")
        elif res_info:
            raise ValidationError("号码已经存在")
        else:
            return txt_mobile
        

def add_number(request):
    if request.method == "GET":
        form = NumberForm():
        return render(request, 'add_number.html', {'form':form})
    elif request.method == "POST":
        form = NumberForm(data=request.POST)
        if form.is_vaild():
            from.save()
            redirect ("/phone_list/")
        else:
            return render(request, 'add_number.html', {'form':form})
       	  
```

```python
# urls.py
urlpatterns = [
    path('phone_list/', views.phone_list),
    path('add_phone/', views.add_phone),
]
```

#### 功能（3）- 编辑靓号

* URL
* 编写view函数
* 编写模板

```python
# urls.py
urlpatterns = [
    path('<int:pk>/update_phone/', views.update_phone)
]
```

```python
# views.py
class FixNumber(forms.ModelForm):
    mobile = froms.CharFiled(disabled=True, label="手机号")
    class meta:
        model = models.PhoneNumber
        field = "__all__"
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs):
            for name, field in self.fields.items():
                field.widget.attars = {'class':'form-control', 'placeholder': name}
    
def update_phone(request, pk):
    if request.method == "GET":
        form_data = PhoneNumber.objects.get(id=pk)
        form = FixNumber(data=form_data)
        return render(request, 'update_phone.html', {"form": form})
    elif request.method == "POST":
        form_data = PhoneNumber.objects.get(id=pk)
        form = FixNumber(requst.POST, instance=form)
        return render(request, 'update_phone.html', {"form": form})
```

```html
<!-- 修改数据模板 -->

{% for field in form %}
	{{field.label}}--{{field}}--{{field.errors.0}}
{% endfor %}
```

#### 功能（4）- 删除靓号

```python
# urls.py

urlpatterns = [
    path('delete_phone/', views.delete_phone)
]
```

```python
# views.py

def delete_phone(request, pk):
    if request.method == "GET":
        models.PhoneNumber.objects.get(id=pk).delete()
    	return render('/phone_list/')
```

#### 功能（5）- 禁止重复

* 添加号码时

```python
# views.py

class NumberForm(forms.ModelForm):    
    class Meta:
        model = models.PhoneNumber
        fields = "__all__"
        
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        # 使用钩子函数校验号码是否存在
        res_info = models.PhoneNumber.objects.filter(mobile=txt_mobile).exists()
        if len(txt_mobile) != 11:
            raise ValidationError("格式错误")
        elif res_info:
            raise ValidationError("号码已经存在")
        else:
            return txt_mobile
        
def add_phone(request):
    if request.method == "POST":
        form = NumberForm(data=request.POST)
        if form.isvaild():
            form.save()
            redirect('/phone_list/')
```

* 编辑号码时

  需要排除自己以外的号码

```python
# views.py

class FixNumberForm(forms.ModelForm):
    class Meta:
        model = models.PhoneNumber
        fields = "__all__"
        
    def clean_mobile(self):
        text_mobile = self.cleand_data['mobile']
        res_info = models.PhoneNumber.objects.exclude(id=self.instance.pk).filter(mobile=text_mobile).exists()
        if len(txt_mobile) != 11:
            raise ValidationError("格式错误")
        elif res_info:
            raise ValidationError("号码已经存在")
        else:
            return txt_mobile
        
def update_phone(request, pk):
    if request.method == "POST":
        phone_info = models.objects.filter("id=pk")
        form = FixNumberForm(data=request.POST, instance=phone_data)
        if form.valid():
            form.save()
            return redirect("/phone_list/")
        else:
            return render(request, 'update_phone.html', {"form": form})
```

#### 功能（6）- 搜索靓号

除了直接过滤之外还可以过滤字典

```python
data_dict = {"mobile": "15620939846", "id": 5}
models.PhoneNumber.objects.filter(**data_dict)

# 过滤数值比较
models.PhoneNumber.objects.filter(id=12) # 等于12
models.PhoneNumber.objects.filter(id__gt=12) # 大于12
models.PhoneNumber.objects.filter(id__gte=12) # 大于等于12
models.PhoneNumber.objects.filter(id__lt=12) # 小于12
models.PhoneNumber.objects.filter(id__lte=12) # 小于等于12

# 过滤字符串
models.PhoneNumber.objects.filter(mobile__startwith="123") # 以123开头
models.PhoneNumber.objects.filter(mobile__endtwith="123") # 以123结尾
models.PhoneNumber.objects.filter(mobile__contains="123") # 包涵123
```

```python
# views.py

def filter_phone(request):
    if request.method == "GET":
        data_dict = {}
        res_content = request.GET.get("content")
        if res_content:
            data_dict['mobile__contains'] = res_content
        search_content = models.objects.filter(**data_dict)
        return render(request, 'phone_list.html', {'search_content':search_content})
    # 注意template 模板中的数据也要对应修改为 search_content
```

```html
<!-- phone_list.html -->
<form method="get">
    <div class="input-group mb-3">
        <input type="search" class="form-control" placeholder="请输入搜索内容..."
               aria-label="Recipient's username" aria-describedby="button-addon2" name="content">
        <button class="btn btn-outline-secondary" type="submit" id="button-addon2"><i class="bi bi-search"></i></button>
    </div>
</form>
```

#### 功能（7）- 列表分页

```python
# views.py
def filter_phone(request):
    if request.method == "GET":
        data_dict = {}
        pagesize = 2
        res_content = request.GET.get("content")
        if res_content:
            data_dict["mobile__contains"] = res_content
        search_content = models.objects.filter(**data_dict)

        # 分页操作
        search_content = search_content[(pagenum-1) * pagesize : pagenum * pagesize]
        return render(request, 'phone_list', {'search_content': search_content})
```

```python
# 直接使用django自带的分页模块
from django.core.paginator import Paginator
from django.shortcuts import render
from myapp.models import Contact

def listing(request):
    contact_list = Contact.objects.all()
    paginator = Paginator(contact_list, 25) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'list.html', {'page_obj': page_obj})

# 可以自己封装一个分页方法，待实现！
```

### 管理员系统

#### 功能（1）- 管理员列表

```python
# models.py 

class Admin(models.Model):
    username = models.CharFiled(verbose_name="管理员账号", max_length=32)
    password = models.CharFiled(verbose_name="密码", max_length=64)
 	
    def __str__(self):
        return self.username
```

```python
# views.py
from . import models

def admin_list(request):
    
    queryset = models.Admin.objects.all()
    return render(request, 'admin_list.html', {"admin_list": queryset})
```

```python
# urls.py
urlpatterns = [
    path('/admin_list/', views.admin_list)
]
```

#### 功能（2）- 新建管理员

```python
# 编写md5校验模块

import hashlib
from django.conf import settings

def md5(data_string):
    obj = hashlib.md5(settings.SCRET_KEY.encode('utf-8'))  # 盐,盐用的是django自己生成的密钥
    obj = obj.update(data_string.encode('utf-8')) # 将密码惊醒md5加密,然后加盐
    # 返回加密后的密码字符串
    return obj.hexdigest()
```



```python
# view.py

class AdminModelForm(forms.ModelForm):
    confirm_password = Froms.CharFiled(label="确认密码"， max_length=64, forms.widget=PasswordInput)
    
    class Meta:
        model = models.Admin()
        fields = ['username', 'password', 'confirm_password']
        
        wigets = {
            "password":forms.PasswordInput
        }
    
    # 使用钩子函数对密码进行加密, 钩子函数是按照顺序执行的
    def clean_password(self):
        pwd = self.cleaned_data["password"]
        # 加密措施
        pwd = md5(pwd)
        return pwd
    
    # 使用钩子函数进行密码一致性校验
    def clean_confirm_password(self):
        c_pwd = self.cleaned_data["confirm_data"]  # 需要对确认的密码同样进行加码
        c_pwd = mdt(pwd)
        pwd = self.cleaned_data["password"]        # 这里的密码已经是加密过的
        if c_pwd != pwd:
            raise VlidationError("密码输入不一致")
        return c_pwd
     

def add_admin(request):
    if request.method == "GET":
        form = AdminModelForm()
        returen render(request, 'add_admin.html', {'form':form})
    elif request.method = "POSt":
        form = AdminModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            returen redirect('/admin/')
        else:
            return render(request, 'add_admin.html', {'from': form})
```

```python
# urls.py

urlpatterns = [
    path('/add_admin/', views.add_admin)
]
```

#### 功能（3）- 管理员编辑

```python
# views.py

def update_admin(request, aid):
    if request.method == "GET":
        admin_data = models.Admin.objects.get(id=aid)
        if amin_data: # 判断aid是否存在
            form = AdminModelForm(intance=admin_data)
            return render(request, 'add_base.html', {'form': form})
        else:
            return redirect('/admin_list/')
    elif request.methd == "POST":
        admin_data = models.Admin.objects.get(id=aid)
        form = AdminModelForm(instance=admin_data, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin_list/')
        else:
            return render(request, 'add_base.html', {'form':form})        
```

```python
# urls.py

urlpatterns = [
    path('<int:aid>/update_admin/', views.update_admin)
]
```

#### 功能（4）- 管理员删除

```python
# views.py

def delete_admin(request, aid):
    if request.method == "GET":
        models.Admin.objects.get(id=aid).delete()
       	return redirect('/admin_list/')
```

#### 功能（5）- 重置密码

* 注意重置密码时不允许与原密码相同

```python
# views.py

class ResetPasswordForm(forms.ModelForm):
    # 控制开关
    flag = True
        
    confirm_password = forms.CharField(
        label="确认密码",
        max_length=64,
        widget=forms.PasswordInput
    )
    
    class Meta:
        model = models.Admin
        filelds = ['password']
        widgets = {
            "password": forms.PasswordInput
        }
        
    def clean_password(self):
        pwd = self.cleaned_data["password"]
        pwd = md5(pwd)
        old_pwd = models.Admin.objects.filter(id=self.instance.pk, password=pwd).exists()
        if old_pwd:
            self.flag = False
            raise ValidationError("不能使用旧密码")
        return pwd
            
    
    def clean_confirm_password(self):
        if not self.flag
        	self.flag = True
        	return self.cleaned_data["confirm_data"]
        c_pwd = self.cleaned_data["confirm_data"]
        c_pwd = md5(c_pwd)
        pwd = self.cleaned_data["password"]
        if c_pwd == pwd:
            return c_pwd
        else:
            raise ValidationError('用户名密码不一致')
        

def reset_password(request, aid):
    if request.method == "GET":
        admin_info = models.Admin.objects.get(id=aid)
        form = AdminModelForm(instance=admin_info)
        return render(request, 'add_base.html', {'form': form})
    elif request.method == "POST":
        admin_info = models.Admin.objects.get(id-aid)
        form = AdminModelForm(instance=admin_info, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin_list/')
        else:
            return render(request, 'add_base.html', {'form':form})
```

```python
# urls.py

urlpatterns = [
    path('<int:aid>/reset_password/', views.reset_password)
]
```

### 用户登录

http协议是无状态 & 短链接

* cookie

  * cookie 是保存在浏览器端的键值对

  * cookie 在浏览器发送请求时会自动携带

* session

  * session 是存储用户信息的的一种方式，有很多种存储方式（包括：数据库，radis，文件）
  * django 中session默认是存储在数据库中的

#### 功能（1）- 用户登录

```python
# views.py

class LoginForm(forms.Form):
    
    username = forms.CharFiled(
        max_length=32,
        widget=forms.TextInput(),
        require=True
    )
    
    password = forms.CharField(
    	max_length=64,
        widget=form.PasswordInput(),
        require=True
    )
    
    def clean_password(self):
        pwd = self.clean_data.get("password")
        pwd = mdt(pwd)
        return pwd
    

def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'from':form})
    elif request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid()
        	user_data = models.Admin.objects.get(**models.clean_data)
            if user_data:
                """
                1.验证成功跟以后网站生成随机字符串写入到cookie中
                2.然后再将随机字符串写入到session中
                3.request.session["info"] = {'id':user_data.id,'name':user_data.username} 使用该条语句进行存储
                """
				request.session["info"] = {'id':user_data.id, 'name':user_data.username}
				return redirect('/users/')
            else:
                form.add_error('password',"用户名或密码错误，请重新输入")
        return render(request, 'login.html', {'form':form})
		
```

#### 功能（2）- 用户认证

```python
# views.py

def amin_list(request):
    """
    1.检查用户是否已经登录，已登录，继续向下走，未登录，跳转回到登录页面
    2.用户发来请求，获取cookie随机字符串，拿到随机字符串到session中进行比对
    3.使用request.session.get('info')获取到session
    """
    info = request.session.get('info')
    if not info:
        return redirect('/login/')
```

##### 认识中间件

```python
# middleware/auth

from django.utils.deprecation import MiddlewareMixin

class M1(MiddlewareMixin):
    """中间件1"""
    def process_request(self, request):
        print('m1 is coming')
        # 如果没有返回值默认返回None,这个时候中间件将向后继续运行
        # 如果有返回值则直接返回运行
    def process_response(self, request, response):
        print('m1 is going')
        return response
class M1(MiddlewareMixin):
    """中间件2"""
    def process_request(self, request):
        print('m1 is coming')
    def process_response(self, request, response):
        print('m1 is going')
        return response
```

在settings中进行中间件注册

```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app01.middleware.auth.m1',
    'app01.middleware.auth.m2'
]
```

#### 功能（3）- 校验登录

编写中间件

```python
# middleware/auth.py

class AuthMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        print('启动用户校验')
        # 排除掉不需要验证就可以访问的页面
        if request.path_info == '/login/':
            return
        """读取当前访问用户的信息"""
        is_login = request.session.get('info').exists()
        if not is_login:
            retrun redirect('/login/')
        return None
    def process_response(self, request, response):
        print('完成了用户校验')
        return response
```

注册中间件

```python
# settins.py
MIDDLEWARE=[
    ...,
    'app01.middleware.auth.LoginMiddleware',
]
```

#### 功能（4）- 用户注销

```python
# views.py

def logout(request):
    if request.method == "GET":
       	# 清除session
        request.session.clear()
        return redirect('/login/')
```

#### 功能（5）- 验证码

##### 生成图片

```python
# 安装pillow
pip install pillow
```

验证码生成原理

* 取出随机数字和字母
* 将字母和随机数写在画布上
* 在画布上随机添加点和干扰线

```python
from PIL from import Image, ImageDraw, ImageFont

img = Image.new(mode='RGB', size=(120, 30), color=(255, 255, 255)) # 255 255 255 是白色
draw = ImageDraw.Draw(img, mode='RGB')

font - ImageFont.truetype("字体.ttf", 28)

draw.text([0, 0], 'python', 'red')
with open('code.png', 'wb') as f:
    image.save(f, format='png')

```



```python
# veiws.py

def code_image(request):
    # 调用pillow函数生成图片
    img, code_string = check_code()
    
    # 写入到自己的session中以便后面进行校验
    request.session['image_code'] = code_string
    # 给session设置60秒超时
    request.session.set_expiry(60)
    
```

### Ajax请求

浏览器向网站发送请求时：使用 URL 和 Form进行提交

* POST
* GET

这两种提交方式都会导致页面的刷新

除了以上两种请求方式之外还可以使用Ajax的方式进行请求（偷偷进行请求）

* 依赖Jquery
* 编写JavaScript代码

```javascript
$.ajax({
    url: '发送的地址',
    type: 'GET', // 或者POST，代表请求方式
    data:{
        page:1,
        name:lsy,
    }
    // data代表的是传递的参数
    success: function(res){
    	console.log('请求成功')
    	console.log(res)
}
})
```

#### GET请求

```javascript
// 发送GET请求
$.ajax({
    url: '/task/ajax/',
    type: "GET",
    data:{
        n1:123,
        n2:454,
    },
    success:function(res){
        cosole.log(res)
    }
})
```

```python
# views.py
def task_ajax(request):
    if request.method == "GET":
        print(request.GET)
        return HttpResponse('reqest GET success')
```

#### POST请求

```javascript
// 发送post请求
$.ajax({
    url:"/task/ajax",
    type: "POST",
    data:{
        n1:343,
        n2:454
    },
    success:function(res){
        console.log(res)
    }
})
```

```python
# views.py
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def task_ajax(request):
    if request.method == "POST":
        print(request.POST)
        return HttpResponse('request POST success')
```

#### Ajax请求返回值

通常返回的是JSON格式的数据

```python
# views.py
import json
def task_ajax(request):
    if request.method == "GET":
        print(request.GET)
        data_dict = {'status': 200, 'info_list':[
            {'name': 'zs', 'age':18},
            {'name': 'ls', 'age':20},
            {'name': 'ww', 'age':30}
        ]}
        # 将python字典转化为json
        json_dict = json.dumps(data_dict)
        return json_dict
        # 或者可以直接使用django的返回函数
        return JsonResponse(data_dict)
```









 

