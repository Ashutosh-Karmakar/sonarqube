from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

from Accounts.serializers import RegistrationSerializer

from rest_framework.authtoken.models import Token


# @csrf_exempt
@api_view(['POST',])
def register(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['success'] = "Successfully added user"
            data['email'] = account.email
            data['username'] = account.username
            data['token'] = Token.objects.get(user=account).key
        else:
            data = serializer.errors
        return Response(data=data)