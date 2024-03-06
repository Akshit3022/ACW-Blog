from django.urls import path
from django.conf.urls.static import static

from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('forgetPass', views.forgetPass, name='forgetPass'),
    path('resetPass/<str:token>/', views.resetPass, name='resetPass'),
    path('adminDash', views.adminDash, name='adminDash'),
    path('handleUser', views.handleUser, name='handleUser'),
    path('userDeactivate/<int:id>/', views.userDeactivate, name='userDeactivate'),
    path('userActivate/<int:id>/', views.userActivate, name='userActivate'),
    path('home', views.home, name='home'),
    path('myBlog', views.myBlog, name='myBlog'),
    path('changePass', views.changePass, name='changePass'),
    path('content', views.addContent, name='content'),
    path('profile', views.profile, name='profile'),
    path('profile_detail/<int:user_id>/', views.profile_detail, name='profile_detail'),
    path('follow/<int:user_id>/', views.follow, name='follow'),
    path('unfollow/<int:user_id>/', views.unfollow, name='unfollow'),
    path('addComment/<int:pk>/', views.addComment, name='addComment'),
    path('addRating/<int:pk>/', views.addRating, name='addRating'),

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
