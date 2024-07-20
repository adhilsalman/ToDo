from django.shortcuts import render,redirect
from django.views.generic import View
from reminder.forms import register,Signin,Taskform
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from reminder.models import Task
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        else:
            return fn(request,*args,**kwargs)
    return wrapper 

def mylogin(fn):
    def wrapper(request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Task.objects.get(id=id)
        if obj.user!=request.user:
            return redirect('login')
        else:
            return fn(request,*args,**kwargs)
    return wrapper 

dec=[signin_required,mylogin]

class registerview(View):
    def get(self,request,*args,**kwargs):
        form=register()
        return render(request,"reg.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=register(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
        form=register()
        messages.success(request,"Registration successfully done")
        return render(request,"reg.html",{"form":form})
    


class Signview(View):
    def get(self,request,*args,**kwargs):
        form=Signin()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=Signin(request.POST)
        if form.is_valid():
           u_name=form.cleaned_data.get("username")
           pwd=form.cleaned_data.get("password")
           email=form.cleaned_data.get("email")
           user_obj=authenticate(request,username=u_name,password=pwd,email=email)
           print(user_obj)
           if user_obj:
               print("valid")
               login(request,user_obj)
            #    sendmail
               subject='Register Successfull'
               message='thank u for login'
               email_from=settings.EMAIL_HOST_USER
               recipient_list = [user_obj.email]
               send_mail(subject,message,email_from,recipient_list)
               return redirect("index")
           else:
               print("invalid")
        return render(request,"login.html",{"form":form}) 
    
@method_decorator(signin_required,name = "dispatch")
class Taskview(View):
    def get(self,request,*args,**kwargs):
        form=Taskform()
        data=Task.objects.filter(user=request.user).order_by('complete')
        return render(request,"index.html",{"form":form,"data":data})
    
    def post(self,request,*args,**kwargs):
        form=Taskform(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
        else:
            print("get out")
        form = Taskform()
        data=Task.objects.filter(user=request.user)
        return render(request,"index.html",{"form":form,"data":data})
        


class Signout(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("login")

class Taskupdate(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Task.objects.get(id=id)
        if qs.complete == True:
            qs.complete = False
            qs.save()
        elif qs.complete == False:
            qs.complete = True
            qs.save()
        return redirect("index")


@method_decorator(dec,name="dispatch")   
class Taskdel(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Task.objects.filter(id=id).delete()
        messages.success(request,"Employee deleted Successfully")
        return redirect("index")