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
        userEmail = request.POST.get('userEmail')
        userPassword = request.POST.get('userPassword') 

        user = request.user

        if CustomUser.objects.filter(userEmail=userEmail, userPassword=userPassword).exists():  
            request.session['email'] = userEmail
            return redirect('home')
        elif User.objects.filter(email=user.email).exists() and check_password(userPassword, request.user.password):
            request.session['email'] = userEmail
            return redirect('adminDash')
        else:
            # global reset_email 
            # reset_email = request.POST.get('userEmail')
            message = "Either Your Email Address or Password is incorrect...!!!"
            return render(request, "login.html", {'message':message})
                   
    return render(request, 'login.html')

def changePass(request):
    if request.method == 'POST':
        oldPass = request.POST.get('oldPass')
        newPass = request.POST.get('newPass')
        confirmPass = request.POST.get('confirmPass')
        

        user = CustomUser.objects.get(userEmail=request.session['email'])
        print("user.userPassword",user.userPassword)
        if user and oldPass == user.userPassword:
            # if check_password(oldPass, user.userPassword):
            print("old",oldPass)
            if newPass == confirmPass:
                user.userPassword = newPass
                user.save()
                return redirect('login')
            else:
                message = "New Passwords do not match...!!!"
                return render(request, "home.html", {'message':message})
        else:
            message = "Old Passwords do not match...!!!"
            return render(request, "home.html", {'message':message})

    return render(request, 'login.html')

def reset(request):
    # email = reset_email
    return render(request, 'reset.html')

def home(request):
    return render(request, 'home.html')