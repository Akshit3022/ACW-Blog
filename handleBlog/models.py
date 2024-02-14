from django.db import models

# Create your models here.

class CustomUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=100)
    userEmail = models.EmailField()
    userPassword = models.CharField(max_length=100)     
    userPhone = models.CharField(max_length=50)
    userAbout = models.TextField(max_length=1000)

    def __str__(self):
        return self.userName
    
class Blog(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    blog_id = models.AutoField(primary_key=True)
    blogTitle = models.CharField(max_length=100)
    blogImage = models.ImageField()
    blogContent = models.TextField(max_length=10000) 
    blogDate = models.DateTimeField()

    def __str__(self):
        return self.blogTitle

class Comment(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    comment_id = models.AutoField(primary_key=True)
    commentContent = models.TextField(max_length=300)
    commentDate = models.DateTimeField()

    def __str__(self):
        return self.user_id
    
class Rating(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    rating_id = models.AutoField(primary_key=True)
    ratingValue = models.FloatField(null=True)

    def __str__(self):
        return self.user_id