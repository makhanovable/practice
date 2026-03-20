from django.contrib import admin
from django.urls import path

from main.views import main_view, login_view, register_view, activate_view, logout_view, send_mail_view, \
    secret_view

urlpatterns = [
    path('', main_view, name='main'),
    path('admin/', admin.site.urls),
    path('secret/', secret_view, name='secret'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('activate/<str:token>/', activate_view, name='activate')
]
