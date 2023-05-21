
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Postings, Message
from django.db.models import Q
# 若没有登录直接路由到讨论广场

@login_required(login_url= '/topics')
def index(request):

    isactive = 'index'

    posts = Postings.objects.filter(username=request.user.username)

    paginator = Paginator(posts, 3)

    context = {'user':request.user, 'isactive':isactive, 'posts':paginator.get_page(1), 'page':1}

    return render(request, 'web/index.html', context=context)

def topics(request) :

    posts = Postings.objects.all().order_by('?')[:10]

    context = {'isactive':'topics', 'posts':posts}

    return render(request, 'web/topics.html', context=context)


@login_required(login_url='login')
def chat(request, username) :

    opponent = User.objects.get(username=username)
    me = request.user

    messages = Message.objects.filter(
            (Q(sender=opponent, receiver=me) | Q(sender=me, receiver=opponent))
    )
    
    users = getUsers(me.username)

    context = {'isactive':'message','users': users, 'infos':messages, 'opponent':opponent}
    
    return render(request, 'web/message.html', context)

def getUsers(username):

    me = User.objects.get(username=username)

    messages = Message.objects.filter(
        Q(sender=me) | Q(receiver=me)
    )

    users = set()
    
    for message in messages:
        if message.sender == me:
            users.add(message.receiver)
        else:
            users.add(message.sender)

    return list(users)

@login_required(login_url='login')
def message(request):

    users = getUsers(request.user.username)

    context = {'users': users,'isactive':'message'}

    return render(request, 'web/message.html', context)


def loginPage(request):

    page = 'login'

    if request.user.is_authenticated :
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try :
            user = User.objects.get(username=username)
        except:
            messages.error(request, '用户不存在')
        
        user = authenticate(request, username=username, password=password)

        if user is not None :
            login(request, user)
            return redirect('index')
        else :
            messages.error(request,'用户邮箱或密码错误')

    context = {'page': page}
    return render(request, 'web/signin.html', context)

@login_required(login_url='login')
def updateUser(request):
    
    message = ''
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        bio = request.POST.get('bio')
        avator = request.POST.get('avator')

        try :
            user = User.objects.get(username=username)
        
            user.avator = avator
            user.bio = bio
            user.email = email
            
            user.save()

        except :
            message = '更新失败'

    context = {'message': message}

    return render(request, 'web/update_user.html', context) 

# 完成分页
@login_required(login_url= '/login')
def indexGetPage(request) :
    username = request.user.username

    pages = Postings.objects.filter(username=username).order_by('create_time')

    paginator = Paginator(pages, 3)
    page = ''

    if request.method == 'POST':

        page = int(request.POST.get('page'))
        
        next_page = int(request.POST.get('next'))

        if next_page == -1 and paginator.get_page(page).has_previous() :
            page = page + next_page
        elif next_page == 1 and paginator.get_page(page).has_next() :
            page = page + next_page

        else:
            messages.error(request, '不能再往前辣~')
    
    print(paginator.get_page(page).object_list, page)
    context = {'user':request.user, 'isactive':'index', 'posts':paginator.get_page(page).object_list, 'page': page}

    return render(request, 'web/index.html', context=context)

def logoutUser(request) :

    logout(request)
    return redirect('index')

@login_required(login_url='login')
def createPost(request) :

    message = ''

    if request.method == 'POST':
        content = request.POST.get('content')
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        username = request.user.username

        if len(content) == 0 or len(title)  == 0 or len(subtitle) == 0 :
            message = '内容、标题、摘要均不能为空'

        elif len(content) > 10000 or len(title) > 50 or len(subtitle) > 100 :
            message = '内容(10000)、标题(50)、摘要内容过长(100)'
        else :

            Postings.objects.create(
                username=username,
                content=content,
                subtitle=subtitle,
                title=title
            )
            return redirect('index')

    context = {'message':message, 'isactive':'createPost'}

    return render(request, 'web/create_post.html', context)


def postContent(request, id):
    print(id)
    post = Postings.objects.get(id=id)
    print(post)
    return render(request, 'web/post_content.html', {'post':post})

def registerPage(request):
    message = ''
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if len(username) == 0 or len(password1) == 0 or len(password2) == 0 :
            message = '用户名或密码不能为空'

        elif User.objects.filter(username=username).exists() :
            message = '用户名重复'

        elif password1 != password2 :
            message = '两次密码不一致'
        else :
            user = User.objects.create(username=username)
            user.set_password(password1)

            user.save()
        
            authenticate_user = authenticate(username=username, password=password1)
        
            login(request, authenticate_user)
            
            return redirect('index')
    

    return render(request, 'web/signup.html', {'message':message})

