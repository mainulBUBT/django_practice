from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Account.forms import UserForm, UserInfoForm
from Account.models import UserInfo


def index(request):
    dicts = {}
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id
        user_info = User.objects.get(pk=user_id)
        user_more_info = UserInfo.objects.get(user__pk=user_id)
        dicts ={'user_info': user_info, 'user_more_info': user_more_info}

    return render(request, 'Account/index.html', context=dicts)

def register(request):
    registered = False
    
    if request.method == 'POST':
        userForm = UserForm(data=request.POST)
        userInfoFom = UserInfoForm(data=request.POST)

        if userForm.is_valid() and userInfoFom.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            userInfo = userInfoFom.save(commit=False)
            userInfo.user = user

            if 'profile_pic' in request.FILES:
                userInfo.profile_pic = request.FILES['profile_pic']
            
            userInfo.save()
            registered = True
    else:
        userForm = UserForm()
        userInfoFom = UserInfoForm()

    return render(request, 'Account/register.html', context={'userForm':userForm, 'userInfoForm': userInfoFom, 'registered':registered})

def login_page(request):
    return render(request, 'Account/login.html', context={})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('Account:index'))
            else:
                return HttpResponse('User is not active')
        else:
            return HttpResponse('User Details Wrong!')
    else:
        # return HttpResponseRedirect(reverse('Account:login'))
        return redirect(reverse('Account:login'))


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Account:logout'))