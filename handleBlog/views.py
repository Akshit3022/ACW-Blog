from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
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
        print('user',user)

        if CustomUser.objects.filter(userEmail=userEmail, userPassword=userPassword).exists():  
            request.session['email'] = userEmail
            return redirect('home')
        elif User.objects.filter(email=user.email).exists() and check_password(userPassword, request.user.password):
            request.session['email'] = userEmail
            return redirect('adminDash')
        else:
            message = "Either Your Email Address or Password is incorrect...!!!"
            return render(request, "login.html", {'message':message})
                   
    return render(request, 'login.html')

def changePass(request):
    if request.method == 'POST':
        oldPass = request.POST.get('oldPass')
        newPass = request.POST.get('newPass')
        confirmPass = request.POST.get('confirmPass')
    
        user = CustomUser.objects.get(userEmail=request.session['email'])
        
        if user and oldPass == user.userPassword:
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
    return render(request, 'reset.html')

def home(request):
    return render(request, 'home.html')

def blog(request):
    blogs = Blog.objects.all()
    return render(request, 'blog.html', {'blogs':blogs})

def addContent(request):
    if request.method == 'POST':
        date = datetime.date.today()
        blogTitle = request.POST.get('blogTitle')
        blogContent = request.POST.get('blogContent')
        blogImage = request.POST.get('blogImage')

        obj = CustomUser.objects.get(userEmail=request.session['email'])
        user_instance = get_object_or_404(CustomUser, user_id=obj.user_id)

        obj = Blog.objects.create(user_id=user_instance, blogDate=date, blogTitle=blogTitle, blogContent=blogContent, blogImage=blogImage)
        obj.save()
        
        return redirect('blog')

    return render(request, 'content.html')

def author(request):
    authors = CustomUser.objects.all()
    return render(request, 'author.html', {'authors': authors})