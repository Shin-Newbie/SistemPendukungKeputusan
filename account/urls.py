from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.registrasi, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]