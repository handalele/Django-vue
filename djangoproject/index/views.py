import json
import random
from django.core.mail import send_mail
from django.http import JsonResponse
from django.middleware.csrf import get_token
import string
import redis
from .serializers import *


# path("login/", views.login)
def login(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    if username and password:
        user = User.objects.filter(username=username, password=password).first()
        if user:
            # 登录成功，返回token
            print('登录成功')
            token = get_token(request)
            return JsonResponse({'code': 200, 'message': '登录成功', 'username': username, 'token': token, })
        else:
            # 用户名或密码错误
            print('用户名或密码错误')
            return JsonResponse({'code': 400})

    else:
        # 用户名或密码为空
        print('用户名或密码不能为空')
        return JsonResponse({'code': 401, 'message': '用户名或密码不能为空'})


# path("register/", views.register)
def register(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    user_code = data.get('code')
    if username and password:
        if User.objects.filter(username=username).exists():
            # 用户名已存在
            return JsonResponse({'code': 400, 'message': '用户名已存在'})
        elif verify_code(email, user_code):
            # 注册用户，可以使用Django内置的User模型
            user = User(username=username, password=password, email=email)
            user.save()
            # 注册成功
            return JsonResponse({'code': 200, 'message': '注册成功'})
        else:
            # 验证码错误
            return JsonResponse({'code': 400, 'message': '验证码错误'})
    else:
        print('用户名或密码为空')
        # 用户名或密码为空
        return JsonResponse({'code': 400, 'message': '用户名或密码不能为空'})


# 存储验证码到redis
r = redis.Redis(host='localhost', port=6379, db=0)
# 点赞功能利用redis缓存
redis_id = redis.Redis(host='localhost', port=6379, db=1)


def save_verification_code(email, code, expire_time=600):
    r.set(email, code, expire_time)
    return code


# 验证验证码

def verify_code(email, code):
    store_code = r.get(email)
    if store_code and store_code.decode() == code:
        r.delete(email)
        return True
    return False


# 发送邮箱验证码
def send_email(request):
    # ?email
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'code': 400, 'message': '邮箱不能为空'})
    # 生成验证码随机六位阿拉伯数字
    verification_code = ''.join(random.sample(string.digits, 6))
    print(verification_code)
    # 发送验证码
    send_mail('验证码',
              message=f'【乐仔博客】尊敬的用户，您的验证码为：{verification_code}，请在10分钟内输入验证码完成注册。如非本人操作，请忽略此短信。',
              recipient_list=[email],
              from_email='2177446547@qq.com')
    save_verification_code(email, verification_code)
    return JsonResponse({'code': 200, 'message': '验证码发送成功'})


# path("blog/", views.content)
# 获取全部博客信息
def content(request):
    username = request.GET.get('username')
    user_id = User.objects.get(username=username).id
    contents = Content.objects.all()
    serializer = ContentSerializer(contents, many=True)
    for content_data in serializer.data:
        content_data['is_upvoted'] = has_user_upvoted(user_id, content_data['id'])
    return JsonResponse({'code': 200, 'message': '获取博客信息成功', 'data': serializer.data})


# 检查用户是否已经点赞过这篇文章
def has_user_upvoted(user_id, content_id):
    return Upvote.objects.filter(people_id=user_id, essay_id=content_id).exists()


# path("upvote/", views.upvote),
# 点赞功能实现
# def upvote(request):
#     data = json.loads(request.body)
#     content_id = data.get('content_id')
#     username = data.get('user_id')
#     # print(username, content_id)
#     people = User.objects.get(username=username)
#     content = Content.objects.get(id=content_id)
#     try:
#         upvote = Upvote.objects.get(people_id=people.id, essay_id=content.id)
#         # 如果已经点赞，则取消点赞
#         upvote.delete()
#         message = '取消点赞成功'
#         content_up = Content.objects.get(id=content_id)
#         content_up.up -= 1
#         new_up = content_up.up
#         content_up.save()
#         return JsonResponse({'code': 201, 'message': message, 'up': new_up})
#     except Upvote.DoesNotExist:
#         # 如果没有点赞过，则创建点赞记录
#         Upvote.objects.create(people_id=people.id, essay_id=content.id)
#         message = '点赞成功'
#         content_up = Content.objects.get(id=content_id)
#         content_up.up += 1
#         new_up = content_up.up
#         content_up.save()
#         return JsonResponse({'code': 200, 'message': message, 'up': new_up})
def upvote(request):
    data = json.loads(request.body)
    content_id = data.get('content_id')
    username = data.get('user_id')
    print(username, content_id)
    if r.sismember(f'user:{username}:upvoted_contents', content_id):
        # 如果已经点赞，则取消点赞
        r.srem(f'user:{username}:upvoted_contents', content_id)
        r.srem(f'content:{content_id}:upvotes', username)
        # 更新内容的点赞数
        r.decr(f'content:{content_id}:up_number')
        message = '取消点赞成功'
    else:
        # 如果没有点赞过，则创建点赞记录
        r.sadd(f'user:{username}:upvoted_contents', content_id)
        r.sadd(f'content:{content_id}:upvotes', username)
        # 更新内容的点赞数
        r.incr(f'content:{content_id}:up_number')
        message = '点赞成功'

        # 获取更新后的点赞数
    new_up = r.get(f'content:{content_id}:up_number')
    return JsonResponse({'code': 200 if message == '点赞成功' else 201, 'message': message, 'up': int(new_up)})


# path("publish/", views.publish),
# 发布博客
def publish(request):
    data = json.loads(request.body)
    title = data.get('title')
    content_type = data.get('content_type')
    substance = data.get('content')  # 文章
    username = data.get('user')
    print(title, content_type, username)
    if title and content_type and substance and username:
        author = User.objects.get(username=username)
        # 创建博客
        content_blog = Content(title=title, content_type=content_type, content=substance, author=author)
        content_blog.save()
        return JsonResponse({'code': 200, 'message': '发布成功'})
    else:
        return JsonResponse({'code': 400, 'message': '发布失败'})


# path("blog/<int:blog_id>/", views.blog_detail),
# 获取博客详情
def blog_detail(request, blog_id):
    content_detail = Content.objects.get(id=blog_id)
    serializer = ContentSerializer(content_detail)
    return JsonResponse({'code': 200, 'message': '获取博客详情成功', 'data': serializer.data})


# path("comment/", views.comment)
# 添加评论
def comment(request):
    data = json.loads(request.body)
    username = data.get('author')
    content_id = data.get('content')
    comment_says = data.get('comment')
    user = User.objects.get(username=username)
    blog_id = Content.objects.get(id=content_id)
    if user and blog_id:
        content_comment = Comment(comment=comment_says, author=user, content=blog_id)
        content_comment.save()
        return JsonResponse({'code': 200, 'message': '评论成功'})
    else:
        return JsonResponse({'code': 400, 'message': '评论失败'})


# path("comment/<int:comment_id>/", views.comment_detail),
# 获取评论 返回评论的用户名，评论的什么评论时间
def comment_detail(request, content_id):
    print(content_id)
    content_detail = Comment.objects.filter(content_id=content_id)
    serializer = CommentSerializer(content_detail, many=True)
    return JsonResponse({'code': 200, 'message': '获取评论成功', 'data': serializer.data})


# path("user/home/<str:username>", views.home),
# 获取个人所有博客包括标题，内容，发布时间，点赞量，收藏量
def home(request, username):
    print(username)
    user = User.objects.get(username=username)
    content_detail = Content.objects.filter(author_id=user.id)
    serializer = ContentSerializer(content_detail, many=True)
    return JsonResponse({'code': 200, 'message': '获取个人所有博客成功', 'data': serializer.data})


# path("delete/<int:content_id>", views.delete),
# 删除博客
def delete(request, content_id):
    content_delete = Content.objects.get(id=content_id)
    content_delete.delete()
    return JsonResponse({'code': 200, 'message': '删除成功'})


# path("update/<int:content_id>", views.update),
# 修改博客
def update(request, content_id):
    data = json.loads(request.body)
    title = data.get('title')
    content_type = data.get('content_type')
    substance = data.get('content')  # 文章
    username = data.get('user')
    if title and content_type and substance and username:
        author = User.objects.get(username=username)
        content_update = Content.objects.get(id=content_id)
        content_update.title = title
        content_update.content_type = content_type
#
# def csrf_token(request):
#     token = get_token(request)
#     return JsonResponse({'csrf_token': token})
#
#
# def test(request):
#     if request.method == 'GET':
#         return JsonResponse({'status': 'success', 'message': 'Data received'})
#     elif request.method == 'POST':
#         try:
#             # ... 您的其他处理逻辑 ...
#             return JsonResponse({'status': 'success', 'message': 'Password received'})
#         except KeyError:
#             return JsonResponse({'status': 'error', 'message': 'Password not found in request'}, status=400)
