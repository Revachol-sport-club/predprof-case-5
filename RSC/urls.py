from django.contrib import admin
from django.urls import path, include
from index import views
urlpatterns = [
    path('', views.index, name='main_page'),
    path('applications/', include('applications.urls')),
    path('app_auth/', include('app_auth.urls')),
    path('inventory_editing/', include('inventory_editing.urls')),
]
