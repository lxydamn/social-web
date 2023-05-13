
import random
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Postings

# 若没有登录直接路由到讨论广场

@login_required(login_url= '/topics')
def index(request):

    isactive = 'index'

    posts = Postings.objects.filter(username=request.user.username)

    context = {'user':request.user, 'isactive':isactive, 'posts':posts}

    return render(request, 'web/index.html', context=context)

def topics(request) :

    posts = Postings.objects.all().order_by('?')[:10]

    context = {'isactive':'topics', 'posts':posts, 'topics_active':'commend'}

    return render(request, 'web/topics.html', context=context)

def topics_recent(request) :

    posts = Postings.objects.all().order_by('-create_time')

    context = {'isactive':'topics', 'posts':posts[:10], 'topics_active':'recent'}

    return render(request, 'web/topics.html', context=context)

def topics_hot(request) :

    posts = Postings.objects.all()[:10]

    context = {'isactive':'topics', 'posts':posts, 'topics_active':'hot'}

    return render(request, 'web/topics.html', context=context)



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

def logoutUser(request) :
    logout(request)
    return redirect('index')

def createPost(request) :

    return render(request, 'web/create_post.html', {'isactive':'createPost'})


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

