# D:\web\midbizsolution\midbizsolution\urls.py

from django.contrib import admin
from django.urls import path, include
from . import views  # views.py 파일에서 함수들을 import
# 추가된 부분
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('secure-admin/', admin.site.urls),
    path('plantlayout/', include('plantlayout.urls')),
    path('pemledger/', include('pemledger.urls')),
    path('pecstandard/', include('pecstandard.urls')),
    path('', views.home, name='home'),  # 루트 URL에 'home' 뷰 함수 연결, base.html 렌더링
    path('greetings/', views.greetings, name='greetings'),  # greetings.html 렌더링
    path('checkpoint/', views.checkpoint, name='checkpoint'),  # checkpoint.html 렌더링
    path('doc-index/', views.doc_index, name='doc_index'),  # doc_index.html 렌더링
    path('solutions/', views.solutions, name='solutions'),  # solutions.html 렌더링
]

# 추가된 부분: 정적 파일 제공 설정
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)