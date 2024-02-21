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
    path('home', views.home, name='home'),
    path('myBlog', views.myBlog, name='myBlog'),
    path('changePass', views.changePass, name='changePass'),
    path('content', views.addContent, name='content'),
    path('addComment/<int:pk>/', views.addComment, name='addComment'),

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
