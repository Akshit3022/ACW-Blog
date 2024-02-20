from django.urls import path
from django.conf.urls.static import static

from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('reset', views.reset, name='reset'),
    path('adminDash', views.adminDash, name='adminDash'),
    path('handleUser', views.handleUser, name='handleUser'),
    path('userDeactivate/<int:id>/', views.userDeactivate, name='userDeactivate'),
    path('home', views.home, name='home'),
    path('myBlog', views.myBlog, name='myBlog'),
    path('changePass', views.changePass, name='changePass'),
    path('content', views.addContent, name='content'),
    path('addComment/<int:pk>/', views.addComment, name='addComment'),

    path('resetPassword/', auth_views.PasswordResetView.as_view(template_name='resetPassword.html'), name='resetPassword'),
    path('resetPasswordDone/', auth_views.PasswordResetDoneView.as_view(template_name='resetPasswordDone.html'), name='resetPasswordDone'),
    path('resetPasswordConfirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='resetPasswordConfirm.html'), name='resetPasswordConfirm'),
    path('resetPasswordComplete/', auth_views.PasswordResetCompleteView.as_view(template_name='resetPasswordComplete.html'), name='resetPasswordComplete'),

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
