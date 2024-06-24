from django.urls import path
from . import views

urlpatterns = [
    # 登录
    path("login/", views.login, name='登录'),
    # 注册
    path("register/", views.register, name='注册'),
    # 发送验证码
    path("code/", views.send_email, name='发送验证码'),
    # 获取博客信息
    path("blog/user", views.content),
    # 发布博客
    path("publish/", views.publish),
    # 点赞功能实现
    path("upvote/", views.upvote),

    # 获取博客详情
    path("detail/<int:blog_id>/", views.blog_detail),
    # 评论功能实现
    path("comment/", views.comment),
    # 获取评论详情
    path("comment/detail/<int:content_id>/", views.comment_detail),
    # 获取个人首页博客信息
    path("user/home/<str:username>", views.home),
    # 删除博客
    path("delete/<int:content_id>", views.delete),
    # 修改博客
    path("update/<int:content_id>", views.update),

    # path("token/", views.csrf_token),
    # path("db/", views.db_test),
    # path("add/", views.add_book),
    # path("qurry/", views.qurry_book),
    # path("filter/", views.filter_book),
    # path("update/", views.update_book),
    # path("delete/", views.delete_book),
]
