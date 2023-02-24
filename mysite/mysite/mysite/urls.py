"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('user/user_list', views.user_list),
    path('template/show_template', views.show_template),
    path('unicom/news', views.unicom_new),
    path('net_request/', views.net_request),
    path('login/', views.login),
    path('users/', views.show_users),
    path('delete_info/', views.delete_user),
    path('add_user/', views.add_user),
    path('add_user2/', views.add_user2),
    path('<int:pk>/update_user2/', views.update_user2),
    path('<int:pk>/delete_user2/', views.delete_user2),
    path('phone_list/', views.phone_list),
    path('add_phone/', views.add_phone),
    path('<int:pk>/update_phone/', views.update_phone),
    path('<int:pk>/delete_phone/', views.delete_phone)
]
