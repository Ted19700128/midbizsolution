#!-- D:/web/midbizsolution/pfcstandard/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_pfcs, name='create_pfcs'),
    path('searchpopup/', views.show_search_popup, name='show_search_popup'),
    path('menu/', views.pfcs_menu, name='pfcs_menu'),  # pfcs_menu 뷰 함수와 URL 이름 설정
]