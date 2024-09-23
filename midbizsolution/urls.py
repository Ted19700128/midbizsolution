#!-- D:/web/midbizsolution/midbizsolution/urls.py

from django.contrib import admin
from django.urls import path, include  # include를 추가하여 각 앱의 urls.py를 포함할 수 있도록 함

urlpatterns = [
    path('secure-admin/', admin.site.urls),  # Django 관리자 페이지 URL
    path('pemledger/', include('pemledger.urls')),  # 설비 점검 기준서 관련 URL
    path('pecstandard/', include('pecstandard.urls')),  # 설비 점검 기준서 관련 URL
]