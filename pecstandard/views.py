#!-- D:/web/midbizsolution/pecstandard/views.py

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db import transaction
from .models import PECS
from .forms import CreateDocumentForm, UpdateDocumentForm
from django.contrib import messages
from pemledger.models import ManagementTeam    # <== 새로 추가됨(0922)
from django.http import JsonResponse
from pemledger.models import Equipment  # Equipment 모델이 pemledger에 있다고 가정

def show_management_teams(request):        # <== 새로 추가됨(0922)
    management_teams = ManagementTeam.objects.all()
    return render(request, 'pecstandard/management_team_list.html', {'management_teams': management_teams})

def filter_by_management_team(request):    # <== 새로 추가됨(0922)
    management_team_id = request.GET.get('management_team')
    if management_team_id:
        documents = PECS.objects.filter(management_team_id=management_team_id)
    else:
        documents = PECS.objects.all()

    return render(request, 'pecstandard/pecs_all_main.html', {'documents': documents})

def get_management_team(request):
    equipment_number = request.GET.get('equipment_number')
    if equipment_number:
        # equipment_number를 사용하여 pemledger의 Equipment 모델에서 관련 정보를 가져옴
        equipment = get_object_or_404(Equipment, equipment_number=equipment_number)
        management_team = equipment.management_team.name  # management_team 필드가 Equipment에 있다고 가정
        return JsonResponse({'management_team': management_team})
    return JsonResponse({'error': 'Invalid equipment number'}, status=400)

def show_search_popup(request):
    management_teams = ManagementTeam.objects.all()  # 모든 관리부서 가져오기  # <== 수정됨(0922)
    return render(request, 'pecstandard/searchpopup.html', {'management_teams': management_teams})

def pecs_all_main(request):
    # 모든 PECS 문서를 가져옵니다.
    documents = PECS.objects.all()
    
    # 템플릿으로 전달할 컨텍스트 데이터
    context = {
        'create_pecs': reverse('create_pecs'),
        'documents': documents,  # 문서 목록을 템플릿에 전달
    }

    return render(request, 'pecstandard/pecs_all_main.html', context)

def create_pecs(request):
    if request.method == 'POST':
        form = CreateDocumentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pecs_all_main')
    else:
        form = CreateDocumentForm()
    return render(request, 'pecstandard/create_pecs.html', {'form': form})

def pecs_change_main(request, document_id):
    document = get_object_or_404(PECS, id=document_id)

    if request.method == 'POST':
        form = UpdateDocumentForm(request.POST, instance=document)
        print(request.POST)  # POST 데이터를 출력하여 확인
        if form.is_valid():
            form.save()
            messages.success(request, "문서가 성공적으로 업데이트되었습니다.")
            return redirect('pecs_all_main')
        else:
            print(form.errors)  # 오류 출력
            messages.error(request, f"입력한 정보에 오류가 있습니다: {form.errors}")
    else:
        form = UpdateDocumentForm(instance=document)
    return render(request, 'pecstandard/pecs_change_main.html', {'form': form, 'document': document})

def delete_pecs(request, document_id):
    document = get_object_or_404(PECS, id=document_id)
    
    if request.method == 'POST':
        # 'confirm_delete' 버튼이 클릭되었을 때 장비 삭제
        if 'confirm_delete' in request.POST:
            document.delete()
            messages.success(request, "문서가 성공적으로 삭제되었습니다.")
            return redirect('pecs_all_main')  # 삭제 후 메뉴 페이지로 리디렉션
        else:
            return redirect('pecs_all_main')  # '아니오' 버튼 클릭 시 메뉴 페이지로 리디렉션
    
    return render(request, 'pecstandard/delete_pecs.html', {'documents': [document]})

def pecs_main_table(request, document_id):
    # document_id를 사용하여 PECS 객체를 가져옴
    document = get_object_or_404(PECS, id=document_id)
    return render(request, 'pecstandard/pecs_main_table.html', {'document': document})