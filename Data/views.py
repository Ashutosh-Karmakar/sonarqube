from django.shortcuts import render
from django.http import HttpResponse

from .models import Names
from django.views.decorators.csrf import csrf_exempt
from Data.serializers import NameSerializer

from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


from Accounts.models import NewUser


#Names.objects refer to the whole database and .all() gives all the objects 
def home(request):
    names = Names.objects.all()
    return render(request,'home.html',{"names":names})

@csrf_exempt #csrf_exempt will exempt all the security on reaching this url from any domain
@api_view(['GET',]) #this ensures only get request is reached upto this and nothing else and also give access to request the attributes like user data etc
@permission_classes((IsAuthenticated,))#It checks wheather u have the permission to user this method or not on the basis of the authentication method provided
# in the settings.py here we are using token authentication so it checks the token first
def api_get(request,name):
    if request.method == 'GET':
        try:
            names = Names.objects.get(name=name)
        except Names.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = NameSerializer(names) #this gives the object of the serializer class and we can perform the operation of its parent class and also the data from the database it is linked to
        return Response(serializer.data)# it send the response in the form of json format
    
@csrf_exempt
@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_put(request,name):
    if request.method == 'PUT':
        try:
            names = Names.objects.get(name=name) #find the Names database with name as name provided in url
        except Names.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user = request.user #gets whih user is trying to access this method from the token automatically 
        # print(user)
        if names.author != user: #checks if this user is the author of the post
            return Response({'response':"you donot have permission to edit this"})
        serializer = NameSerializer(names,data = request.data) #makes changes to the database with names as object with the data provides
        data = {}
        if serializer.is_valid(): # if the serializer object is valid then save it to the database
            serializer.save()
            data['success'] = "Successfully updated the data"
            return Response(data)
        else:
            return Response(serializer.error,status=status.HTTP_404_NOT_FOUND)
@csrf_exempt
@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def api_delete(request,name):
    if request.method == 'DELETE':
        try:
            names = Names.objects.get(name=name)
        except Names.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user = request.user
        # print(user)
        if names.author != user:
            return Response({'response':"you donot have permission to edit this"})
        operation = names.delete() #delete the table with names as object from database Names and it returns None if unsuccessfull
        data = {}
        if operation:
            data['success'] = "Deleted successfully"
        else:
            data['Failuer'] = "Deletion could not be done"
        return Response(data=data)
    
@csrf_exempt
@api_view(['POST'],)
@permission_classes((IsAuthenticated,))
def api_post(request):
    if request.method == 'POST':
        # accounts = NewUser.objects.get(pk = 1)
        accounts = request.user #gets which user has added from the post from the token 
        namepost = Names(author=accounts) #create a new object of the database with the given author 
        serializer = NameSerializer(namepost,data = request.data)#add this object to the database
        if serializer.is_valid():#if adding is succesfull then save
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.error,status = status.HTTP_404_BAD_REQUEST)
        
        
