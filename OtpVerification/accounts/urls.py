from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('otp/', views.otp_page, name='otp'),
    path('logout/', views.logout_page, name='logout'),
    path('login-otp/', views.login_otp, name='login_otp'),
]
