from io import BytesIO
import pandas as pd
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.db import transaction
from .models import Equipment
from .forms import EquipmentForm

def landing_page(request):
    return render(request, 'landing_page.html')

def translation(request):
    return render(request, 'translation.html')

def music(request):
    return render(request, 'music.html')

def travel(request):
    return render(request, 'travel.html')

def solutions(request):
    return render(request, 'solutions.html')

def equipment_list(request):
    equipments = Equipment.objects.all()
    return render(request, 'myapp/equipment_list.html', {'equipments': equipments})

def equipment_list_edit(request):
    equipments = Equipment.objects.all()
    return render(request, 'myapp/equipment_list_edit.html', {'equipments': equipments})

def equipment_menu(request):
    mode = request.GET.get('mode', 'view')
    show_table = True  # 항상 테이블을 표시하도록 설정
    equipments = Equipment.objects.all() if show_table else None
       
    if mode == 'edit':
        equipment_id = request.GET.get('equipment_id')  # GET 파라미터에서 가져오기
        if equipment_id:
            equipment = get_object_or_404(Equipment, id=equipment_id)
            update_url = reverse('update_equipment', args=[equipment.id])
            return redirect(update_url)
        else:
            return redirect('equipment_list_edit_mode')  # 적절한 URL 이름으로 변경
    
    context = {
        'create_equipment': reverse('create_equipment'),
        'mode': mode,
        'show_table': show_table,
        'equipments': equipments,
    }

    return render(request, 'myapp/equipment_menu.html', context)

def create_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            # 설비 번호 자동 부여 (예: PF001 형식)
            last_equipment = Equipment.objects.order_by('id').last()
            if last_equipment:
                last_equipment_number = last_equipment.equipment_number
                new_equipment_number = f'PF{int(last_equipment_number[2:]) + 1:03d}'
            else:
                new_equipment_number = 'PF001'
                    
            # 새 설비 생성
            new_equipment = form.save(commit=False)
            new_equipment.equipment_number = new_equipment_number
            new_equipment.save()

            return redirect('equipment_menu')  # 생성 후 설비 목록 페이지로 리다이렉트
    else:
        form = EquipmentForm()
    
    return render(request, 'myapp/create_equipment.html', {'form': form})

def update_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            # messages.success(request, "장비가 성공적으로 업데이트되었습니다.")
            return redirect('equipment_list_edit_mode')  # 적절한 URL 이름으로 변경
        else:
            messages.error(request, "입력한 정보에 오류가 있습니다.")
            # 추가된 코드: 폼 오류를 템플릿에 전달
            return render(request, 'myapp/update_equipment.html', {'form': form, 'equipment': equipment})
    else:
        form = EquipmentForm(instance=equipment)
    
    context = {
        'form': form,
        'equipment': equipment,
    }
    
    return render(request, 'myapp/update_equipment.html', context)

def delete_confirmation(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)  # 장비가 존재하는지 확인
    
    if request.method == 'POST':
        # 'confirm_delete' 버튼이 클릭되었을 때 장비 삭제
        if 'confirm_delete' in request.POST:
            equipment.delete()  # 장비 삭제
            messages.success(request, "장비가 성공적으로 삭제되었습니다.")
            return redirect('equipment_list_edit_mode')  # 삭제 후 장비 목록으로 리디렉션
        else:
            return redirect('equipment_list_edit_mode')  # '아니오' 버튼 클릭 시 장비 목록으로 리디렉션
    
    return render(request, 'myapp/delete_confirmation.html', {'equipments': [equipment]})

def delete_equipment(request):
    if request.method == 'POST':
        equipment_ids = request.POST.getlist('equipment_ids')
        if equipment_ids:
            if 'confirm_delete' in request.POST:
                Equipment.objects.filter(id__in=equipment_ids).delete()
                messages.success(request, "선택한 설비가 삭제되었습니다.")
            else:
                messages.info(request, "삭제가 취소되었습니다.")
            return redirect('equipment_list_edit_mode')
        else:
            messages.error(request, "삭제할 설비를 선택하세요.")
            return redirect('equipment_list_edit_mode')
    return redirect('equipment_menu')

def export_to_excel(request):
    filename = request.GET.get('filename', 'equipment_list.xlsx')
    equipments = Equipment.objects.all()

    # 데이터프레임 생성
    data = [
        {
            '설비 번호': equipment.equipment_number,
            '설비명': equipment.name,
            '제조사': equipment.manufacturer,
            '설비 사양': equipment.specs,
        }
        for equipment in equipments
    ]

    df = pd.DataFrame(data)

    # 엑셀 파일을 메모리에 생성
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)  # 파일 포인터를 시작 위치로 이동

    # HttpResponse에 엑셀 파일 작성
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


def equipment_list_edit_mode(request):
    equipments = Equipment.objects.all()  # 모든 장비 목록을 가져옵니다.
    
    # 장비 선택 후 수정할 수 있도록 URL 생성 시 equipment_id 인수를 추가합니다.
    if request.method == 'POST':
        selected_id = request.POST.get('equipment_id')  # 사용자가 선택한 장비의 ID를 가져옵니다.
        if selected_id:
            return redirect('update_equipment', equipment_id=selected_id)  # equipment_id를 전달하여 URL 생성
        else:
            messages.error(request, "수정할 장비를 선택하세요.")
    
    return render(request, 'myapp/equipment_list_edit.html', {'equipments': equipments})

def health_check(request):
    return HttpResponse("OK", content_type="text/plain")
