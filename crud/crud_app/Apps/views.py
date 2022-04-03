from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from Apps.forms import CrudForm

def index(request):
    
    form = CrudForm()
    dictn = {"form":form}
    if request.method == 'POST':
        form = CrudForm(data = request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            mobile = form.cleaned_data.get("mobile")
            dictn = {
                'form': form,
                'name': name,
                'mobile': mobile,
            } 

    print(dictn)
    return render(request, 'index.html', context=dictn)
