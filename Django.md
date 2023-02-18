# Django

## 安装Django

```cmdline
pip install django=="4.0"
```

## 创建项目

```cmdline
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

```cmdline
# ./mysite
python manage.py startapp app01
```

### APP文件

```
├─app01
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  tests.py
│  │  views.py
│  │  __init__.py
│  │
│  └─migrations
│          __init__.py

```

