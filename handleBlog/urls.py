from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    # path('register', views.register, name='register'),
    # path('logout', views.logout, name='logout'),
    # path('home', views.home, name='home'),
    # path('post', views.post, name='post'),
    # path('post/<int:id>', views.post_detail, name='post_detail'),
]
