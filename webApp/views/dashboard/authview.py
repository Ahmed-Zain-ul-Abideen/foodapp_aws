
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http.response import Http404
import json
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User

from django.http import JsonResponse
from twilio.rest import Client
from django.conf import settings
from decouple import config
from django.utils.crypto import get_random_string
from django.utils import timezone
import datetime 
import sys, os
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login,logout




class LoginForm(APIView):
    
    permission_classes = [] 
    def get(self, request):
        context = {'error_flag':False}
        return render(request, 'dashboard/Auth/login.html',context)
    


def UserLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate the user using Django's built-in function
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # if user.is_superuser: 
            #     print("aw super user")
            login(request, user)
            try:
                remember = request.POST['remember_me']
                print("remember",remember)
                if remember:
                    print("remember true")
                    request.session.set_expiry(11124567)
            except: 
                print("remember false")
                
            return redirect('index')
            # else:
            #     print("aw not  super user")
            #     error_message = "Only Super User can access admin panel !"
            #     return render(request, 'dashboard/Auth/login.html', {'error_message': error_message,'error_flag':True})
        else:
            error_message = "Invalid login credentials. Please try again."
            return render(request, 'dashboard/Auth/login.html', {'error_message': error_message,'error_flag':True})
    else:
        return render(request, 'dashboard/Auth/login.html')
    


def UserLogOut(request):
    logout(request)
    return redirect('login-dashboard')

def permissionview(request):

    return render(request, 'dashboard/permission_denied.html')
