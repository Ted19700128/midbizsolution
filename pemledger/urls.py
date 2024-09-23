# D:/web/midbizsolution/pemledger/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('pemledger/all/', views.pemledger_all_main, name='pemledger_all_main'),  # 전체 설비 관리 메인 페이지
    path('pemledger/create/', views.create_pemledger, name='create_pemledger'),  # 설비 신규 생성 페이지
    path('pemledger/change/<int:equipment_id>/', views.change_pemledger, name='change_pemledger'),  # 설비 수정 페이지
    path('pemledger/delete/<int:equipment_id>/', views.delete_pemledger, name='delete_pemledger'),  # 설비 삭제 페이지

    path('pemledger/change/', views.pemledger_change_main_mode, name='pemledger_change_main_mode'),  # 설비 변경 메인 페이지

    # 아래 두 줄을 추가하여 pemledger_change_table 및 pemledger_change_delete URL을 정의
    path('pemledger/change/table/<int:equipment_id>/', views.change_pemledger, name='pemledger_change_table'),  # 설비 수정 (테이블 형식)
    path('pemledger/delete/table/<int:equipment_id>/', views.delete_pemledger, name='pemledger_change_delete'),  # 설비 삭제 (테이블 형식)

    path('pemledger/export/', views.export_to_excel, name='export_to_excel'),  # 엑셀 내보내기
    path('health/', views.health_check, name='health_check'),  # 헬스 체크
]
