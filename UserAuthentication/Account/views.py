from django.shortcuts import render
from Account.forms import UserForm, UserInfoForm


def index(request):
    return render(request, 'Account/index.html', context={})

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