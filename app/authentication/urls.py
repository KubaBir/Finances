from django.urls import path

from .views import login_user, logout_user, register_user

app_name = 'authentication'

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
