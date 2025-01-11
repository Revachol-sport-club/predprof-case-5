from django.contrib import admin
from django.urls import path, include
from .views import applications_user, application_create, applications_admin
urlpatterns = [
    path('user', applications_user, name="applications_user"),
    path('user/create/<int:instr_id>', application_create, name="application_create"),
    path('user/<int:error>', applications_user, name="applications_user"),
    path('admin', applications_admin, name="applications_admin")
]