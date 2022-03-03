from django.shortcuts import render
from django.contrib.auth.models import User
from accounts.models import Profile
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import random
from twilio.rest import Client
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def send_otp(mobile,otp):
    account_sid = ''
    auth_token = ''

    client = Client(account_sid, auth_token)
    message = client.messages.create(
                    body=f"Your otp is- {otp}",
                    from_='+15074795363',
                    to=f'+88{mobile}'
                 )
    print(message.sid)



def login_page(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')

        otp = str(random.randint(1000,9999))
        profile = Profile.objects.filter(mobile=mobile).first()
        
        if profile:
            print(profile.otp)
            profile.otp = otp
            profile.save()
            send_otp(mobile,otp)
            request.session['mobile'] = mobile
            return HttpResponseRedirect(reverse('accounts:login_otp'))
          
    return render(request, 'accounts/login.html', context={})


def login_otp(request):

    mobile = request.session['mobile']

    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
        if profile.otp == otp:
            messages.success(request, "OTP Verification Successfull", extra_tags='success')
            user = User.objects.get(id=profile.user.id)        
            login(request, user)
            return HttpResponseRedirect(reverse('cart:home'))
        else:
            messages.success(request, "Wrong OTP", extra_tags='danger')
            return HttpResponseRedirect(reverse('accounts:otp'))
    return render(request, 'accounts/login_otp.html', context={'mobile':mobile})

def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        try:
            user = User.objects.filter(username=username).first()
            profile = Profile.objects.filter(mobile=mobile).first()
            if user:
                messages.warning(request, "User already exists")
                return HttpResponseRedirect(reverse('accounts:register'))
            elif profile:
                messages.warning(request, "User mobile exists")
                return HttpResponseRedirect(reverse('accounts:register'))

            user = User.objects.create(username=username, email=email)
            user.save()

            otp = str(random.randint(1000,9999))
            profile_obj = Profile.objects.create(user=user, mobile=mobile, otp = otp)
            profile_obj.save()
            print(profile_obj)
            if user and profile_obj:
                send_otp(mobile,otp)
                request.session['mobile'] = mobile
                messages.info(request, "Account Created", extra_tags='success')
                return HttpResponseRedirect(reverse('accounts:otp'))
        except Exception as e:
            print(e)
    return render(request, 'accounts/register.html', context={})


def otp_page(request):
    mobile = request.session['mobile']
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()

        if profile.otp == otp:
            messages.success(request, "OTP Verification Successfull", extra_tags='success')
            user = User.objects.get(id=profile.user.id)        
            login(request, user)
            return HttpResponseRedirect(reverse('cart:home'))
        else:
            messages.success(request, "Wrong OTP", extra_tags='danger')
            return HttpResponseRedirect(reverse('accounts:otp'))

    return render(request, 'accounts/otp.html', context={'mobile':mobile})

@login_required
def logout_page(request):
    logout(request)
    messages.success(request, "logged out", extra_tags='success')
    return HttpResponseRedirect(reverse('accounts:login'))
