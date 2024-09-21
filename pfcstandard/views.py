#!-- D:/web/midbizsolution/pfcstandard/views.py

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db import transaction
from .models import PFCS
from .forms import CreateDocumentForm, UpdateDocumentForm
from django.contrib import messages

def pfcs_menu(request):
    mode = request.GET.get('mode', 'view')
    documents = PFCS.objects.all()
    
    if mode == 'edit':
        document_id = request.GET.get('document_id')  # GET 파라미터에서 가져오기
        if document_id:
            update_url = reverse('update_pfcs', args=[document_id])
            return redirect(update_url)
        else:
            return redirect('pfcs_menu')  # document_id가 없으면 메뉴로 리다이렉트
    
    context = {
        'create_pfcs': reverse('create_pfcs'),
        'mode': mode,
        'documents': documents,
    }

    return render(request, 'pfcstandard/pfcs_menu.html', context)

def create_pfcs(request):
    if request.method == 'POST':
        form = CreateDocumentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pfcs_menu')
    else:
        form = CreateDocumentForm()
    return render(request, 'pfcstandard/create_pfcs.html', {'form': form})

def update_pfcs(request, document_id):
    document = get_object_or_404(PFCS, id=document_id)

    if request.method == 'POST':
        form = UpdateDocumentForm(request.POST, instance=document)
        print(request.POST)  # POST 데이터를 출력하여 확인
        if form.is_valid():
            form.save()
            messages.success(request, "문서가 성공적으로 업데이트되었습니다.")
            return redirect('pfcs_menu')
        else:
            print(form.errors)  # 오류 출력
            messages.error(request, f"입력한 정보에 오류가 있습니다: {form.errors}")
    else:
        form = UpdateDocumentForm(instance=document)
    return render(request, 'pfcstandard/update_pfcs.html', {'form': form, 'document': document})

def delete_pfcs(request, document_id):
    document = get_object_or_404(PFCS, id=document_id)
    
    if request.method == 'POST':
        # 'confirm_delete' 버튼이 클릭되었을 때 장비 삭제
        if 'confirm_delete' in request.POST:
            document.delete()
            messages.success(request, "문서가 성공적으로 삭제되었습니다.")
            return redirect('pfcs_menu')  # 삭제 후 메뉴 페이지로 리디렉션
        else:
            return redirect('pfcs_menu')  # '아니오' 버튼 클릭 시 메뉴 페이지로 리디렉션
    
    return render(request, 'pfcstandard/delete_pfcs.html', {'documents': [document]})

def pfcs_detail(request, document_id):
    # document_id를 사용하여 PFCS 객체를 가져옴
    document = get_object_or_404(PFCS, id=document_id)
    return render(request, 'pfcstandard/pfcs_detail.html', {'document': document})