from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from reminder.models import Task
from api.serializer import Taskserializer,userserializer
from rest_framework import authentication,permissions

    

class Taskviewset(ViewSet):

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    def list(self,request,*args,**kwargs):
        qs=Task.objects.all()
        serializer=Taskserializer(qs,many=True)
        return Response(data=serializer.data)
    
    def create(self,request,*args,**kwargs):
        serializer=Taskserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()   
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Task.objects.get(id=id)
        serilaizer=Taskserializer(qs)
        return Response(data=serilaizer.data)
    
    def update(self,request,*args,**kwargs): 
        id=kwargs.get("pk")
        qs=Task.objects.get(id=id)
        serializer=Taskserializer(data=request.data,instance=qs)
        if serializer.is_valid():
            serializer.save()   
            return Response(serializer.data)

    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Task.objects.get(id=id)
        if qs.user==request.user:
            qs.delete()
            return Response()
        return Response("login user doesnt match")
    
class SignUpView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=userserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)