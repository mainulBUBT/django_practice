from unicodedata import name
from django.shortcuts import render

# Create your views here.

def login_page(request):
    return render(request, 'accounts/login.html', context={})

def register_page(request):
    return render(request, 'accounts/register.html', context={})

def otp_page(request):
    return render(request, 'accounts/otp.html', context={})
