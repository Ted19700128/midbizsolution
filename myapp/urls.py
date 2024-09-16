from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_equipment, name='create_equipment'),  # 설비 생성 페이지
    path('', views.equipment_list, name='equipment_list'),  # 설비 목록 페이지
    path('health/', views.health_check, name='health_check'),  # / 경로에 대해 간단한 "OK" 응답 반환
]