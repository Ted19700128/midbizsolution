from django.contrib import admin
from django.urls import path, include  # include를 추가하여 각 앱의 urls.py를 포함할 수 있도록 함

urlpatterns = [
    path('admin/', admin.site.urls),  # Django 관리자 페이지 URL
    path('', include('myapp.urls')),  # myapp의 urls.py를 포함]
]