from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cart.urls')),
    path('account/', include('accounts.urls')),
]