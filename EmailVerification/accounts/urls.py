from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_attempt, name='login'),   
    path('register/', views.register_attempt, name='register'),
    path('verify/<auth_token>', views.verify, name='verify'),
    path('token/', views.token_send, name='token_send'),
    path('success/', views.success, name='success'),
    path('error/', views.error_page, name='error'),
    path('logout/', views.logout_attempt, name='logout'),
]
