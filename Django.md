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

