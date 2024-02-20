from django.urls import path
from django.conf.urls.static import static

from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login, name='login'),
    path('register', views.register, name='register'),
    path('reset', views.reset, name='reset'),
    path('home', views.home, name='home'),
    path('myBlog', views.myBlog, name='myBlog'),
    path('changePass', views.changePass, name='changePass'),
    path('author', views.author, name='author'),
    path('content', views.addContent, name='content'),
    path('addComment/<int:pk>/', views.addComment, name='addComment'),

    path('resetPassword/', auth_views.PasswordResetView.as_view(template_name='resetPassword.html'), name='resetPassword'),
    path('resetPasswordDone/', auth_views.PasswordResetDoneView.as_view(template_name='resetPasswordDone.html'), name='resetPasswordDone'),
    path('resetPasswordConfirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='resetPasswordConfirm.html'), name='resetPasswordConfirm'),
    path('resetPasswordComplete/', auth_views.PasswordResetCompleteView.as_view(template_name='resetPasswordComplete.html'), name='resetPasswordComplete'),
    # path('logout', views.logout, name='logout'),
    # path('post', views.post, name='post'),
    # path('post/<int:id>', views.post_detail, name='post_detail'),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
