from django.contrib import admin
from . models import *


# Register your models here.
class CustomUserModelAdmin(admin.ModelAdmin):
    list_display = ["user_id", "userName", "userEmail", "userPassword", "userImage", "is_active"]
admin.site.register(CustomUser, CustomUserModelAdmin)

class BlogModelAdmin(admin.ModelAdmin):
    list_display = ["user_id","blog_id", "blogTitle", "blogDate"]
admin.site.register(Blog, BlogModelAdmin)

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ["user_id", "blog_id", "comment_id", "commentersName", "commentContent", "commentDate"]
admin.site.register(Comment, CommentModelAdmin)

class RatingModelAdmin(admin.ModelAdmin):
    list_display = ["user_id", "blog_id", "rating_id", "ratingValue"]
admin.site.register(Rating, RatingModelAdmin)

class UserProfileModelAdmin(admin.ModelAdmin):
    list_display = ["user"]
admin.site.register(UserProfile, UserProfileModelAdmin)
