from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from . models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
import datetime
from django.core.files.storage import FileSystemStorage
from .handleEmail import sendForgetPassMail
import uuid


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
        # print('user',user)

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


def adminDash(request):
    blogs = Blog.objects.all()
    comments = Comment.objects.all()
    return render(request, 'adminDash.html' ,{'blogs':blogs, 'comments':comments})


def handleUser(request):

    authors = CustomUser.objects.all()
    return render(request, 'handleUser.html', {'authors': authors})


def userDeactivate(request, id):
    user = CustomUser.objects.filter(user_id=id)
    user.delete()
    return redirect(handleUser)

def home(request):

    blogs = Blog.objects.all()
    comments = Comment.objects.all()
    return render(request, 'home.html', {'blogs':blogs, 'comments':comments})


def myBlog(request):

    users = CustomUser.objects.get(userEmail=request.session['email'])
    user_instance = get_object_or_404(CustomUser, user_id = users.user_id)

    myblogs = Blog.objects.filter(user_id=user_instance)
    return render(request,'myBlog.html', {'myblogs':myblogs})


def addContent(request):

    if request.method == 'POST':    
        date = datetime.date.today()
        blogTitle = request.POST.get('blogTitle')
        blogContent = request.POST.get('blogContent')
        blogImage = request.FILES.get('blogImage')
        # print('blog Image ',blogImage)

        obj = CustomUser.objects.get(userEmail=request.session['email'])
        user_instance = get_object_or_404(CustomUser, user_id=obj.user_id)

        obj = Blog.objects.create(user_id=user_instance, blogDate=date, blogTitle=blogTitle, blogContent=blogContent, blogImage=blogImage)
        fs = FileSystemStorage()
        filename = fs.save(blogImage.name, blogImage)
        uploaded_img_url = fs.url(filename)
        obj.blogImage = uploaded_img_url
        obj.save()

        return redirect('home')

    return render(request, 'content.html')


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
                return render(request, "changePass.html", {'message':message})
        else:
            message = "Old Passwords do not match...!!!"
            return render(request, "changePass.html", {'message':message})

    return render(request, 'changePass.html')


def forgetPass(request):

    if request.method == 'POST':
        userEmail = request.POST.get('userEmail')

        user = CustomUser.objects.get(userEmail=userEmail)

        if user:
            token = str(uuid.uuid4())
            print("token", token)
            sendForgetPassMail(user.userEmail, token)
            message = "An Email is Sent."
            return render(request, "forgetPass.html", {'message':message, 'token':token})
        else:
            message = "User does not exist...!!!"
            return render(request, "forgetPass.html", {'message':message})  
        
    return render(request, 'forgetPass.html')


def resetPass(request, token):
    context = {}
    try:
        user = CustomUser.objects.get(forgetPassToken = token)
        print(user)
    except Exception as e:
        print(e)
    return render(request, 'resetPass.html')



def addComment(request, pk):

    if request.method == 'POST':    
        
        commentContent = request.POST.get('commentContent')

        obj = CustomUser.objects.get(userEmail=request.session['email'])       
        # print(pk)
        user_instance = get_object_or_404(CustomUser, user_id=obj.user_id)
        blog_instance = get_object_or_404(Blog, blog_id=pk)
        # print("BI ",blog_instance)

        obj = Comment.objects.create(blog_id=blog_instance, user_id=user_instance, commentersName=obj.userName, commentContent=commentContent)

        return redirect('home')
    
    blog_instance = get_object_or_404(Blog, blog_id=pk)
    comments = Comment.objects.filter(blog_id=blog_instance)

    return render(request, 'home.html', {'blog_instance': blog_instance, 'comments': comments})


def logout(request):
    del request.session['email']
    return redirect('login')