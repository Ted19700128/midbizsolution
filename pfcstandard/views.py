#!-- D:/web/midbizsolution/pfcstandard/views.py

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db import transaction
from .models import PFCS
from .forms import CreateDocumentForm, UpdateDocumentForm
from django.contrib import messages
from myapp.models import ManagementTeam    # <== 새로 추가됨(0922)
from django.http import JsonResponse
from myapp.models import Equipment  # Equipment 모델이 myapp에 있다고 가정

def show_management_teams(request):        # <== 새로 추가됨(0922)
    management_teams = ManagementTeam.objects.all()
    return render(request, 'pfcstandard/management_team_list.html', {'management_teams': management_teams})

def filter_by_management_team(request):    # <== 새로 추가됨(0922)
    management_team_id = request.GET.get('management_team')
    if management_team_id:
        documents = PFCS.objects.filter(management_team_id=management_team_id)
    else:
        documents = PFCS.objects.all()

    return render(request, 'pfcstandard/pfcs_menu.html', {'documents': documents})

def get_management_team(request):
    equipment_number = request.GET.get('equipment_number')
    if equipment_number:
        # equipment_number를 사용하여 myapp의 Equipment 모델에서 관련 정보를 가져옴
        equipment = get_object_or_404(Equipment, equipment_number=equipment_number)
        management_team = equipment.management_team.name  # management_team 필드가 Equipment에 있다고 가정
        return JsonResponse({'management_team': management_team})
    return JsonResponse({'error': 'Invalid equipment number'}, status=400)

def show_search_popup(request):
    management_teams = ManagementTeam.objects.all()  # 모든 관리부서 가져오기  # <== 수정됨(0922)
    return render(request, 'pfcstandard/searchpopup.html', {'management_teams': management_teams})

def pfcs_menu(request):
    # 모든 PFCS 문서를 가져옵니다.
    documents = PFCS.objects.all()
    
    # 템플릿으로 전달할 컨텍스트 데이터
    context = {
        'create_pfcs': reverse('create_pfcs'),
        'documents': documents,  # 문서 목록을 템플릿에 전달
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