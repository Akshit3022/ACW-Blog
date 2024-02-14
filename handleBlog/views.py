from django.shortcuts import render, redirect, HttpResponse
from . models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
import datetime

# Create your views here.

# Admin = yudiz@gmail.com
# pass = Rare9999


def register(request):
    if request.method == 'POST':

        email = request.POST.get('email')

        if CustomUser.objects.filter(userEmail=email).exists():
            return HttpResponse("User Already Exists")

        userName = request.POST.get('userName')
        userEmail = request.POST.get('userEmail')
        userPassword = request.POST.get('userPassword')
        userPhone = request.POST.get('userPhone')
        userAbout = request.POST.get('userAbout')

        user = CustomUser(userName=userName, userEmail=userEmail, userPassword=userPassword, userPhone=userPhone, userAbout=userAbout)
        user.save()
        request.session['email'] = email
        return redirect('login')
    
    return render(request,'register.html')

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