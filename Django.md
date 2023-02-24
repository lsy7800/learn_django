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
        super().__init__(self, *args, **kargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': name}
        

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

def update_phone(request, pk):
    if request.method == "GET":
        form_data = PhoneNumber.objects.get(id=pk)
        form = NumberForm(data=form_data)
        return render(request, 'update_phone.html', {"form": form})
    elif request.method == "POST":
        form_data = PhoneNumber.objects.get(id=pk)
        form = NumberForm(requst.POST, instance=form)
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









