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

```python
# models.py
class User(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharFiled(max_length=64)
    age = models.IntegerFiled()
    phone_number = models.CharFiled(max_length=11)
    
    def __str__:
        return self.username
```



```python
# views.py
def user_list(request):
    if request.method == "GET":
        # 请求数据
        user_list = models.User.objects.all()
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
    
def user_delete(request):
    # 删除数据
    pk = request.GET.get("id")
    print(pk)
    models.UserList.objects.filter(id=pk).delete()

    return redirect("/users/")
```

```python
# urls.py

urlpatterns = [
    path("users/", views.user_list),
    path("user_delete/", views.user_delete),
]
```

```html
<!-- users.html -->
	<h1>用户列表</h1>
	<table class="table table-dark">
		<thead>
		<tr>
			<th>姓名</th>
			<th>密码</th>
			<th>年龄</th>
			<th>电话</th>
			<th>操作</th>
		</tr>
		</thead>
		{% for user in users %}
		<tr>
			<td>{{user.name}}</td>
			<td>{{user.password}}</td>
			<td>{{user.age}}</td>
			<td>{{user.phone_number}}</td>
			<td><a href="/delete_info/?id={{user.id}}">删除数据</a></td>
		</tr>
		{% endfor %}
	</table>

	<form action="/users/" method="post" class="input-area">
		{% csrf_token %}
		<label>用户名</label>
		<input type="text" name="name"/>
		<label>密码</label>
		<input type="text" name="password"/>
		<label>年龄</label>
		<input type="text" name="age"/>
		<label>电话号码</label>
		<input type="text" name="phone_num"/>
		<button type="submit" class="btn btn-primary">添加用户信息</button>
	</form>
```



