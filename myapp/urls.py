from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),  # 홈 페이지 URL 패턴 추가
    path('equipment/', views.equipment_list, name='equipment_list'),  # 설비 목록 페이지
    path('equipment/create/', views.create_equipment, name='create_equipment'),  # 설비 생성 페이지
    path('health/', views.health_check, name='health_check'),  # /health/ 경로에 대한 뷰
]
