"""
URL configuration for ToDo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from reminder.views import registerview,Signview,Taskview,Taskupdate,Taskdel,Signout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',registerview.as_view(),name="reg"),
    path('login/',Signview.as_view(),name='login'),
    path('index/',Taskview.as_view(),name="index"),
    path('index/edit/<int:pk>',Taskupdate.as_view(),name="edit"),
    path('index/del/<int:pk>',Taskdel.as_view(),name="del"),
    path('logout/',Signout.as_view(),name="logout"),
    path("api/",include("api.urls"))
]
