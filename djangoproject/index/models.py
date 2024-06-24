from django.db import models


#  python manage.py makemigrations
#  python manage.py migrate

#  创建用户模型
class User(models.Model):
    username = models.CharField(max_length=200, null=False)
    password = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=200, null=False)
    email = models.EmailField(max_length=254, unique=True, null=False)


# 创建博客模型
class Content(models.Model):
    # image = models.ImageField(upload_to='images/', null=False)
    title = models.CharField(max_length=30, null=False)
    content_type = models.CharField(max_length=20, null=False)
    content = models.TextField(null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    up = models.IntegerField(default=0)


# 创建评论模型
class Comment(models.Model):
    comment = models.TextField(null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    comment_time = models.DateTimeField(auto_now_add=True)


# 创建点赞模型
class Upvote(models.Model):
    people = models.ForeignKey(User, on_delete=models.CASCADE)
    essay = models.ForeignKey(Content, on_delete=models.CASCADE)

# # 创建收藏模型
# class collect(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     content_id = models.ForeignKey(content, on_delete=models.CASCADE)
#     create_time = models.DateTimeField(auto_now_add=True)
