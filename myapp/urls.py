#!-- D:/web/midbizsolution/myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/edit/', views.equipment_list_edit_mode, name='equipment_list_edit_mode'),
    path('equipment/update/<int:equipment_id>/', views.update_equipment, name='update_equipment'),
    path('equipment/delete/', views.delete_equipment, name='delete_equipment'),
    path('equipment/menu/', views.equipment_menu, name='equipment_menu'),
    path('equipment/create/', views.create_equipment, name='create_equipment'),
    path('translation/', views.translation, name='translation'),
    path('music/', views.music, name='music'),
    path('travel/', views.travel, name='travel'),
    path('solutions/', views.solutions, name='solutions'),
    path('health/', views.health_check, name='health_check'),    
    path('equipment/export/', views.export_to_excel, name='export_to_excel'),
]