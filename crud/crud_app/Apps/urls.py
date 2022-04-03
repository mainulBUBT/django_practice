from django.urls import path
from Apps import views


app_name = 'Apps'

urlpatterns = [
    path('', views.index, name="index"),
]

