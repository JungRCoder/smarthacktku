# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect

from userLogin.forms import UserForm, UserProfileForm, EditUserForm, ForgetForm
from userLogin.models import *
import random
from django.core.mail.message import EmailMessage
from threading import Thread
from django.conf.global_settings import LOGIN_URL

# Create your views here.


def checkVerify_required(fun):
    def auth(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(LOGIN_URL)
        if not request.user.userprofile.checkVerify:  #判斷是否有打驗證碼＃
            return HttpResponseRedirect('/userLogin/checkVerify/')
        return fun(request, *args, **kwargs)
    return auth


def emailThread(request, username, version):
    passwordRandom =  str(random.randint(1000, 9999))
    verifyRandom =  str(random.randint(1000, 9999))
    if version == 'forget':
        user = User.objects.get(username=username)
        user.set_password(passwordRandom)
        user.save()
    userProfile = UserProfile.objects.get(user__username=username)
    userProfile.verifyEmailCode = verifyRandom
    userProfile.checkVerify = False
    userProfile.save()

    subject ='您好,這裡是getOnlineStock驗證信件'
    if version == 'forget':
        messages = '密碼：' + passwordRandom +', ' +'驗證碼：' + verifyRandom
    else:
        messages = '驗證碼：' + verifyRandom
    email = User.objects.get(username=username).email
    email = EmailMessage(subject, messages, to=[email])
    email.send()


def register(request):
    '''
    Register a new user
    '''
    template = 'userLogin/register.html'
    if request.method=='GET':
        return render(request, template, {'userForm':UserForm(),'userProfileForm':UserProfileForm()})
    # POST
    username = request.POST.get('username')
    userForm = UserForm(request.POST)
    userProfileForm = UserProfileForm(request.POST)
    if not (userForm.is_valid() and userProfileForm.is_valid()):
        return render(request, template, {'userForm':userForm,'userProfileForm':userProfileForm})
    user = userForm.save()
    user.set_password(user.password)
    user.save()
    userProfile = userProfileForm.save(commit=False)
    userProfile.user = user
    userProfile.save()
    t = Thread(target=emailThread, args=(request, username, 'register'))
    t.start()
    messages.success(request, '歡迎註冊,立即登入')
    return redirect('main:main')


def login(request):
    '''
    Login an existing user
    '''
    template = 'userLogin/login.html'
    if request.method=='GET':
        auth_logout(request)
        return render(request, template)
    # POST
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username or not password: # Server-side validation
        messages.error(request, '請填資料')
        return render(request, template)
    user = authenticate(username=username, password=password)
    if not user: # authenticate fail
        messages.error(request, '登入失敗')
        return render(request, template)
    if not user.is_active:
        messages.error(request, '帳號已停用')
        return render(request, template)
    # login success
    auth_login(request, user)
    if not request.user.userprofile.checkVerify:
        return redirect('userLogin:checkVerify')

    messages.success(request, '登入成功')
    return redirect('main:main')

def logout(request):
    '''
    Logout the user
    '''
    auth_logout(request)
    messages.success(request, '歡迎再度光臨')
    return redirect('userLogin:login')


@login_required
@checkVerify_required
def profile(request, methods):
    if request.method=='GET':
        if methods=='show':
            messages.success(request, '個人資訊')
            return render(request, 'userLogin/profile.html')
        else:
            user = User.objects.get(username = request.user.username)
            userForm = EditUserForm(instance=user)
            userForm.fields['username'].widget.attrs['readonly']=True
            userProfile = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
            userProfileForm = UserProfileForm(instance=userProfile)
            messages.success(request, '個人資訊編輯')
            return render(request, 'userLogin/profile.html', {'userForm':userForm, 'userProfileForm':userProfileForm})

    # request.method == 'POST':
    email = request.POST.get('email')
    user = User.objects.get(username = request.user.username)
    userForm = EditUserForm(data=request.POST, instance=user)
    userProfile = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
    userProfileForm = UserProfileForm(data=request.POST, instance=userProfile)
    if not (userForm.is_valid() and userProfileForm.is_valid()):
        userForm.fields['username'].widget.attrs['readonly']=True
        messages.success(request, '個人資訊編輯')
        return render(request, 'userLogin/profile.html', {'userForm':userForm,'userProfileForm':userProfileForm})
    if request.user.email != email:
        userProfile = UserProfile.objects.get(user__username=request.user.username)
        userProfile.checkVerify = False
        userProfile.save()
    userForm.save()
    userProfileForm.save()
    t = Thread(target=emailThread, args=(request, request.user.username, 'profile'))
    t.start()
    return HttpResponseRedirect('/userLogin/profile/show/')

@login_required
def password(request):
    if request.method=='GET':
        messages.success(request, '修改密碼')
        return render(request, 'userLogin/password.html')

    # request.method == 'POST':
    oldpassword = request.POST.get('oldpassword')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    user = User.objects.get(username=request.user.username)
    checkPassword = user.check_password(oldpassword)
    
    if checkPassword==False and password!=password2:
        return render(request, 'userLogin/password.html', {'oldPasswordErrorMessage':'密碼輸入錯誤', 'passwordErrorMessage':'密碼不符'})
    elif checkPassword==False:
        return render(request, 'userLogin/password.html', {'oldPasswordErrorMessage':'密碼輸入錯誤'})
    elif password!=password2:
        return render(request, 'userLogin/password.html', {'passwordErrorMessage':'密碼不符'})
    else:
        user = User.objects.get(username=request.user.username)
        user.set_password(password)
        user.save()
        auth_logout(request)
        messages.success(request, '修改密碼成功,重新登入')
        return redirect('userLogin:login')


def forgetpassword(request):
    
    if request.method=='GET':
        userForm = ForgetForm()        
        return render(request, 'userLogin/forgetpassword.html', {'userForm':userForm})
    # request.method == 'POST':
    username = request.POST.get('username')
    email = request.POST.get('email')
    userForm = ForgetForm(data=request.POST)
    if not userForm.is_valid():
        return render(request, 'userLogin/forgetpassword.html', {'userForm':userForm})

    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'userLogin/forgetpassword.html', {'userForm':userForm, 'usernameErrorMessage':'查無此帳號'})
    try:
        User.objects.get(username=username, email=email)
    except User.DoesNotExist:
        return render(request, 'userLogin/forgetpassword.html', {'userForm':userForm, 'username':username,'mailErrorMessage':'mail不符'})
    
    t = Thread(target=emailThread, args=(request, username, 'forget'))
    t.start()
    return render(request, 'userLogin/forgetpassword.html', {'showForgetPasswordMessage':'showForgetPasswordMessage'})

@login_required
def checkVerify(request):
    if request.method=='GET':
        return render(request, 'userLogin/checkVerify.html')

    verifyNumber = request.POST.get('verifyNumber')
    if verifyNumber != request.user.userprofile.verifyEmailCode:
        return render(request, 'userLogin/checkVerify.html', {'verifyErrorMessage':'驗證代碼錯誤！'})
    
    userProfile = UserProfile.objects.get(user__username=request.user.username)
    userProfile.checkVerify = True
    userProfile.save()
    messages.success(request, '登入成功')
    return redirect('main:main')


def init(request):
    #User.objects.all().delete()
    #UserProfile.objects.all().delete()
    if User.objects.filter(username='admin'):
        messages.error(request, '已建立')
        return render(request, 'userLogin/init.html')
    
    # Create the 'admin' account
    admin = User()
    admin.username = 'admin'
    admin.first_name = '管理員'
    admin.set_password('admin')
    admin.email = 'admin@gmail.com'
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    userProfile = UserProfile()
    userProfile.user = User.objects.get(username='admin')
    userProfile.fullName = 'admin'
    userProfile.checkVerify = True
    userProfile.verifyEmailCode = '0000'
    userProfile.save()
    messages.success(request, '管理員建立成功')
    return render(request, 'userLogin/init.html')