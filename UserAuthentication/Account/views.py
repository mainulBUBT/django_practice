from django.shortcuts import render

def index(request):
    return render(request, 'Account/index.html', context={})