from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_equipment, name='create_equipment'),  # 설비 생성 페이지
    path('', views.equipment_list, name='equipment_list'),  # 설비 목록 페이지
]