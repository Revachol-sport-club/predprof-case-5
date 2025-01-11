from django.urls import path
from .views import login_view, profile_view, logout_view, register_view
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView): 
    template_name = 'index.html' 

urlpatterns = [
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
]
  