from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import uuid
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from accounts.models import Profile

# Create your views here.


def home(request):

    return render(request, 'accounts/home.html', context={})


def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        user = authenticate(username=username, password=password)
        
        if user is None:
            messages.success(request, 'User not found!', extra_tags='danger')
            return HttpResponseRedirect(reverse('accounts:login'))
        
        profile_obj = Profile.objects.filter(user=user).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile not verified yet!', extra_tags='danger')
            return HttpResponseRedirect(reverse('accounts:login'))
        
        login(request, user)
        return HttpResponseRedirect(reverse('accounts:home'))

    return render(request, 'accounts/login.html', context={})


def register_attempt(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.filter(username=username, email=email).first()
            print(user)
            if user:
                messages.warning(request, 'Email or username already taken')
                return HttpResponseRedirect(reverse('accounts:register'))
            user_obj = User.objects.create(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()

            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(
                user=user_obj, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email, auth_token)
            return HttpResponseRedirect(reverse('accounts:token_send'))

        except Exception as e:
            print(e)

    return render(request, 'accounts/register.html', context={})


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request,"Account already verified!")
                return HttpResponseRedirect(reverse('accounts:success'))
            else:
                profile_obj.is_verified = True
                profile_obj.save()
                messages.success(request,"Account verification completed!")
                return HttpResponseRedirect(reverse('accounts:success'))
        else:
            messages.warning(request, "Verification error!")
            return HttpResponseRedirect(reverse('accounts:error'))
    except Exception as e:
        print(e)

def success(request):
    return render(request, 'accounts/success.html', context={})

def token_send(request):
    return render(request, 'accounts/token_send.html', context={})

def error_page(request):
    return render(request, 'accounts/error.html', context={})

@login_required
def logout_attempt(request):
    logout(request)
    messages.success(request, 'Logged out successfully!', extra_tags='danger')
    return HttpResponseRedirect(reverse('accounts:login'))

def send_mail_after_registration(email, token):
    subject = 'Account verification mail'
    message = f'Click the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)