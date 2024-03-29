from audioop import avg
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from . models import *
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
import datetime
from django.core.files.storage import FileSystemStorage
from .handleEmail import sendForgetPassMail
import uuid


# Create your views here.

# Admin = yudiz@gmail.com
# pass = Rare9999   


def register(request):

    if request.method == 'POST':

        userEmail = request.POST.get('userEmail')

        if CustomUser.objects.filter(userEmail=userEmail).exists(): 
            return HttpResponse("User Already Exists")

        userName = request.POST.get('userName')
        userEmail = request.POST.get('userEmail')
        userPassword = request.POST.get('userPassword')
        userPhone = request.POST.get('userPhone')
        userAbout = request.POST.get('userAbout')
        userImage = request.FILES.get('userImage')
        print('user Image ',userImage)

        hashedPassword = make_password(userPassword)

        users = CustomUser.objects.create(userName=userName, userEmail=userEmail, userPassword=hashedPassword, userPhone=userPhone, userAbout=userAbout, userImage=userImage)
        fs = FileSystemStorage()
        filename = fs.save(userImage.name, userImage)   
        uploaded_img_url = fs.url(filename)
        users.userImage = uploaded_img_url
        users.save()
        return redirect('login')    
    
    return render(request,'register.html')



def login(request):

    if request.method == 'POST':    
        userEmail = request.POST.get('userEmail')
        userPassword = request.POST.get('userPassword') 

        try:
            loginUser = CustomUser.objects.get(userEmail=userEmail)
        except Exception as e:
            loginUser = None

        user = request.user

        if CustomUser.objects.filter(userEmail=userEmail).exists() and check_password(userPassword, loginUser.userPassword):  
            if loginUser.is_active == True:
                request.session['email'] = userEmail
                return redirect('home')
            else:
                message = "You are De-activated..!!"
                return render(request, "login.html", {'message':message})
        elif User.objects.filter(email=user.email).exists() and check_password(userPassword, request.user.password):
            request.session['email'] = user.email
            return redirect('adminDash')
        else:
            message = "Either Your Email Address or Password is incorrect...!!!"
            return render(request, "login.html", {'message':message})
                
    return render(request, 'login.html')



# @login_required
def adminDash(request):
    user_email = request.session.get('email')
    if user_email:
        blogs = Blog.objects.all()
        comments = Comment.objects.all()
        return render(request, 'adminDash.html',{'blogs':blogs, 'comments':comments})
    else:
        return redirect('login')



# @login_required
def handleUser(request):
    user_email = request.session.get('email')
    if user_email:
        authors = CustomUser.objects.all()
        return render(request, 'handleUser.html', {'authors': authors})
    else:
        return redirect('login')



# @login_required
def userDeactivate(request, id):
    user = get_object_or_404(CustomUser, user_id=id)
    user.is_active = False
    user.save()
    return redirect(handleUser)



def userActivate(request, id):
    user = get_object_or_404(CustomUser, user_id=id)
    user.is_active = True
    user.save()
    return redirect(handleUser)



# @login_required
def home(request):
    user_email = request.session.get('email')
    if user_email:
        users = CustomUser.objects.all()
        logged_in_user = CustomUser.objects.get(userEmail=user_email)       
        # blogs = Blog.objects.all()
        blogs = Blog.objects.exclude(user_id=logged_in_user)
        comments = Comment.objects.all()
        ratings = Rating.objects.all()
        return render(request, 'home.html', {'blogs':blogs, 'comments':comments, 'ratings':ratings, 'users':users})
    else:
        return redirect('login')



# @login_required
def myBlog(request):
    user_email = request.session.get('email')
    if user_email:
        users = CustomUser.objects.get(userEmail=request.session['email'])
        user_instance = get_object_or_404(CustomUser, user_id = users.user_id)

        myblogs = Blog.objects.filter(user_id=user_instance)
        loggedUser = CustomUser.objects.all()
        return render(request,'myBlog.html', {'myblogs':myblogs, 'loggedUser':loggedUser})
    else:
        return redirect('login')



# @login_required
def addContent(request):
    
    user_email = request.session.get('email')
    if user_email:
        if request.method == 'POST':    
            date = datetime.datetime.now()
            blogTitle = request.POST.get('blogTitle')
            blogContent = request.POST.get('blogContent')
            blogImage = request.FILES.get('blogImage')
            print('blog Image ',blogImage)

            obj = CustomUser.objects.get(userEmail=request.session['email'])
            user_instance = get_object_or_404(CustomUser, user_id=obj.user_id)

            obj = Blog.objects.create(user_id=user_instance, blogDate=date, blogTitle=blogTitle, blogContent=blogContent, blogImage=blogImage)
            fs = FileSystemStorage()
            filename = fs.save(blogImage.name, blogImage)
            uploaded_img_url = fs.url(filename)
            obj.blogImage = uploaded_img_url
            obj.save()

            return redirect('home')
        users = CustomUser.objects.all()
        return render(request, 'content.html', {'users': users})
    else:
        return redirect('login')



# @login_required
def changePass(request):

    user_email = request.session.get('email')
    if user_email:
        if request.method == 'POST':
            oldPass = request.POST.get('oldPass')
            newPass = request.POST.get('newPass')
            confirmPass = request.POST.get('confirmPass')
        
            user = CustomUser.objects.get(userEmail=request.session['email'])
            
            if user and check_password(oldPass, user.userPassword):
                if newPass == confirmPass:
                    user.userPassword = make_password(newPass)
                    user.save()
                    return redirect('login')
                else:
                    message = "New Passwords do not match...!!!"
                    return render(request, "changePass.html", {'message':message})
            else:
                message = "Old Passwords do not match...!!!"
                return render(request, "changePass.html", {'message':message})
        users = CustomUser.objects.all()
        return render(request, 'changePass.html', {'users':users})
    else:
        return redirect('login')



# @login_required
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



# @login_required
def resetPass(request, token):
    user_email = request.session.get('email')
    if user_email:
        # context = {}
        try:
            user = CustomUser.objects.get(forgetPassToken = token)
            print(user)
        except Exception as e:
            print(e)
        return render(request, 'resetPass.html')
    else:
        return redirect('login')



# @login_required
def addComment(request, pk):
    user_email = request.session.get('email')
    if user_email:
        if request.method == 'POST':    
            
            commentContent = request.POST.get('commentContent')

            obj = CustomUser.objects.get(userEmail=request.session['email'])       
            print(pk)
            user_instance = get_object_or_404(CustomUser, user_id=obj.user_id)
            blog_instance = get_object_or_404(Blog, blog_id=pk)
            print("BI ",blog_instance)

            if user_instance.userEmail != blog_instance.user_id.userEmail:
                comments = Comment.objects.create(blog_id=blog_instance, user_id=user_instance, commentersName=obj.userName, commentContent=commentContent)
                comments.save() 
                return redirect('home')
            else:
                return redirect('home')
        
    else:
        return redirect('login')



def addRating(request, pk):
    user_email = request.session.get('email')
    if user_email:
        if request.method == 'POST':
            
            ratingValue = request.POST.get('ratingValue')
            print("Rating Value", ratingValue)
        
            obj = CustomUser.objects.get(userEmail=request.session['email'])
            user_instance = get_object_or_404(CustomUser, user_id=obj.user_id)
            blog_instance = get_object_or_404(Blog, blog_id=pk)
            print("BI ",blog_instance)
            if user_instance.userEmail != blog_instance.user_id.userEmail:
                Rating.objects.update_or_create(blog_id=blog_instance, user_id=user_instance, defaults={'ratingValue': ratingValue})
                return redirect('home')
            else:
                return redirect('home')
    else:
        return redirect('login')     



# @login_required
def logout(request):
    del request.session['email']
    return redirect('login')



def profile(request):
    user_email = request.session.get('email')
    if user_email:
        users = CustomUser.objects.filter(userEmail=user_email)
        user = get_object_or_404(CustomUser, userEmail=user_email)
        user_profile = get_object_or_404(UserProfile, user=user)
        followers_count = user_profile.followers.count()
        Logged_user_followings = UserProfile.objects.filter(followers=user)
        avg_rating = Rating.objects.filter(blog_id__user_id=user)
        j=0
        count = 0
        for i in avg_rating:
            j = j + i.ratingValue
            count += 1 
        if count != 0: 
            x = j/count
        else:
            x=0
        avg = round(x, 2)
        followings = Logged_user_followings.count()
        return render(request, 'profile.html', {'users': users, 'followers_count':followers_count, 'avg':avg, 'followings':followings })
    else:
        return redirect('login')



def profile_detail(request, user_id):
    user_email = request.session.get('email')
    if user_email:
        users = CustomUser.objects.filter(user_id=user_id)  
        loggedUser = CustomUser.objects.filter(userEmail=user_email).first()
        user = get_object_or_404(CustomUser, user_id=user_id)  
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        followers_count = user_profile.followers.count()
        user_followings = UserProfile.objects.filter(followers=user)
        avg_rating = Rating.objects.filter(blog_id__user_id=user)
        j=0
        count = 0
        for i in avg_rating:
            j = j + i.ratingValue
            count += 1 
        if count != 0: 
            x = j/count
        else:
            x=0
        avg = round(x, 2)
        followings = user_followings.count()
        print('followings', followings)
        return render(request, 'profile_detail.html', {'users': users, 'user_profile':user_profile, 'loggedUser':loggedUser, 'followers_count':followers_count, 'avg':avg, 'followings':followings })
    else:
        return redirect('login')



def follow(request, user_id):
    user_email = request.session.get('email')
    if request.method == 'POST' and user_email:
        user_to_follow = get_object_or_404(CustomUser, user_id=user_id)
        following_user = get_object_or_404(CustomUser, userEmail=user_email)
        user_profile, _ = UserProfile.objects.get_or_create(user=user_to_follow)
        user_profile.followers.add(following_user)
        return redirect('profile_detail', user_id=user_id)
    else:
        return redirect('login')



def unfollow(request, user_id):
    user_email = request.session.get('email')
    if request.method == 'POST' and user_email:
        user_to_unfollow = get_object_or_404(CustomUser, user_id=user_id)
        following_user = get_object_or_404(CustomUser, userEmail=user_email)
        user_profile, _ = UserProfile.objects.get_or_create(user=user_to_unfollow)
        user_profile.followers.remove(following_user)
        return redirect('profile_detail', user_id=user_id)
    else:
        return redirect('login')