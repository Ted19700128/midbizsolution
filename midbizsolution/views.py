# D:\web\midbizsolution\midbizsolution\views.py

from django.shortcuts import render

# 각 템플릿 파일을 렌더링하는 뷰 함수
def home(request):
    return render(request, 'base.html')

def greetings(request):
    return render(request, 'greetings.html')

def checkpoint(request):
    return render(request, 'checkpoint.html')

def doc_index(request):
    return render(request, 'doc_index.html')

def solutions(request):
    return render(request, 'solutions.html')
