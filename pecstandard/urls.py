#!-- D:/web/midbizsolution/pecstandard/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 기존 URL 패턴
    path('create/', views.create_pecs, name='create_pecs'),  # create_pfcs -> create_pecs로 변경
    path('main/', views.pecs_all_main, name='pecs_all_main'),  # pfcs_menu -> pecs_all_main로 변경
    path('mainTable/<int:document_id>/', views.pecs_main_table, name='pecs_main_table'),  # pfcs_detail -> pecs_main_table로 변경
    path('change/<int:document_id>/', views.pecs_change_main, name='pecs_change_main'),  # update_pfcs -> pecs_all_main로 변경
    path('delete/<int:document_id>/', views.delete_pecs, name='delete_pecs'),  # delete_pfcs -> delete_pecs로 변경
    # API 경로
    path('api/get-management-team/', views.get_management_team, name='get_management_team'),  # 장비 번호로 관리팀 정보 가져오기
]

