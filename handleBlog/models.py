from django.db import models
from django.utils.timezone import now

# Create your models here.

class CustomUser(models.Model):    
    user_id = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=100)
    userEmail = models.EmailField()
    userPassword = models.CharField(max_length=100)     
    userPhone = models.CharField(max_length=10)
    userAbout = models.TextField(max_length=1000)
    userImage = models.ImageField(upload_to="images/")
    forgetPassToken = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=True)


    
class Blog(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    blog_id = models.AutoField(primary_key=True)    
    blogTitle = models.CharField(max_length=100)
    blogImage = models.ImageField(upload_to="images/")
    blogContent = models.TextField(max_length=10000) 
    blogDate = models.DateTimeField()


class Comment(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    comment_id = models.AutoField(primary_key=True)
    commentersName = models.CharField(max_length=100, null=True)
    commentContent = models.TextField(max_length=300)
    commentDate = models.DateTimeField(default=now)

    
class Rating(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    rating_id = models.AutoField(primary_key=True)
    ratingValue = models.IntegerField(default=0)


# class UserProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     followers = models.ManyToManyField(CustomUser, related_name='following_users', blank=True)
#     following = models.ManyToManyField(CustomUser, related_name='followers_users', blank=True)


# class Follow(models.Model):

#     follower = models.ForeignKey(CustomUser,related_name='user_followers',on_delete=models.CASCADE)
#     following = models.ForeignKey(CustomUser,related_name='user_follows',on_delete=models.CASCADE)

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    followers = models.ManyToManyField(CustomUser, related_name='following', blank=True)
