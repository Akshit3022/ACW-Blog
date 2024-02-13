from django.shortcuts import render, redirect, HttpResponse
from . models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
import datetime

# Create your views here.

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password') 

        user = request.user

        if CustomUser.objects.filter(email=email, password=password).exists():  
            request.session['email'] = email
            return redirect('home')
        elif User.objects.filter(email=user.email).exists() and check_password(password, request.user.password):
            request.session['email'] = email
            return redirect('adminDash')
        else:
            return HttpResponse("Either email or password is incorrect.")
              
    return render(request, 'login.html')