from django.urls import path

from Account import views
app_name = 'Account'

urlpatterns = [
    path('', views.index, name='index'),
]
