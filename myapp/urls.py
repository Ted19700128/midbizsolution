from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('translation/', views.translation, name='translation'),
    path('music/', views.music, name='music'),
    path('travel/', views.travel, name='travel'),
    path('solutions/', views.solutions, name='solutions'),
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/create/', views.create_equipment, name='create_equipment'),
    path('health/', views.health_check, name='health_check'),
    path('equipment/menu/', views.equipment_menu, name='equipment_menu'),
]