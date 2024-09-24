# D:\web\midbizsolution\plantlayout\urls.py

from django.urls import path
from . import views

app_name = 'plantlayout'

urlpatterns = [
    # path('all/', views.playout_all_main, name='playout_all_main'),
    path('main/', views.playout_main, name='playout_main'),
    path('create/', views.create_playout, name='create_playout'),
    path('add/', views.add_playout, name='add_playout'),
    path('edit/', views.edit_playout, name='edit_playout'),
    path('edit/unit/<int:unit_id>/', views.edit_unit, name='edit_unit'),
    # path('update/<int:equipment_id>/', views.update_playout, name='update_playout'),
    path('search/', views.search_playout, name='search_playout'),
    # path('search/results/', views.search_playout_results, name='search_playout_results'),
    path('update_equipment_position/', views.update_equipment_position, name='update_equipment_position'),
]