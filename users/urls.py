from django.contrib import admin
from django.urls import path, include
from .views import users, user_change_state

urlpatterns = [
    path('', users, name="users"),
    path('<int:id>', user_change_state, name="user_change_state")
]