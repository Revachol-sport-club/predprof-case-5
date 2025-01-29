from django.contrib import admin
from django.urls import path, include
from .views import inventory_editing, inventory_edit_instrument, inventory_purchase, inventory_report, inventory_delete_instrument
urlpatterns = [
    path('', inventory_editing, name="inventory_editing"),
    path('<int:id>', inventory_edit_instrument, name="edit_instrument"),
    path('purchase', inventory_purchase, name="inventory_purchase"),
    path('report', inventory_report, name="inventory_report"),
    path('delete/<int:id>', inventory_delete_instrument, name="delete_instrument")
]