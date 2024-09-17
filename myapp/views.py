# myapp/views.py

from io import BytesIO
import pandas as pd
from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
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

def equipment_menu(request):
    mode = request.GET.get('mode', 'view')
    show_table = True  # 항상 테이블을 표시하도록 설정
    equipments = Equipment.objects.all() if show_table else None
       
    if mode == 'edit':
        equipment_id = request.GET.get('equipment_id')  # GET 파라미터에서 가져오기
        if not equipment_id:
            messages.error(request, "변경할 장비의 ID가 제공되지 않았습니다.")
            return redirect('equipment_list_edit_mode')  # 적절한 URL 이름으로 변경
        equipment = get_object_or_404(Equipment, id=equipment_id)
        update_url = reverse('update_equipment', args=[equipment.id])
        return redirect(update_url)
    
    context = {
        'create_equipment': reverse('create_equipment'),
        'mode': mode,
        'show_table': show_table,
        'equipments': equipments,
    }

    return render(request, 'myapp/equipment_menu.html', context)

def update_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, "장비가 성공적으로 업데이트되었습니다.")
            return redirect('equipment_list')  # 적절한 URL 이름으로 변경
        else:
            messages.error(request, "입력한 정보에 오류가 있습니다.")
    else:
        form = EquipmentForm(instance=equipment)
    
    context = {
        'form': form,
        'equipment': equipment,
    }
    
    return render(request, 'myapp/update_equipment.html', context)

def delete_equipment(request):
    if request.method == 'POST':
        equipment_ids = request.POST.getlist('equipment_ids')
        if equipment_ids:
            if 'confirm_delete' in request.POST:
                Equipment.objects.filter(id__in=equipment_ids).delete()
                messages.success(request, "선택한 설비가 삭제되었습니다.")
                return redirect('equipment_menu')
            elif 'cancel_delete' in request.POST:
                messages.info(request, "삭제가 취소되었습니다.")
                return redirect('equipment_menu')
            else:
                equipments = Equipment.objects.filter(id__in=equipment_ids)
                return render(request, 'myapp/delete_confirmation.html', {'equipments': equipments})
        else:
            messages.error(request, "삭제할 설비를 선택하세요.")
            return redirect('equipment_menu')
    else:
        return redirect('equipment_menu')
        
def export_to_excel(request):
    filename = request.GET.get('filename', 'equipment_list.xlsx')
    equipments = Equipment.objects.all()

    # 데이터프레임 생성
    data = []
    for equipment in equipments:
        data.append({
            '설비 번호': equipment.equipment_number,
            '설비명': equipment.name,
            '제조사': equipment.manufacturer,
            '설비 사양': equipment.specs,
        })

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

def create_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if 'confirm_edit' in request.POST:  # 'confirm_edit' 버튼이 눌렸을 때
            if form.is_valid():  # 폼이 유효한 경우
                form.save()  # 폼 저장
                return redirect('equipment_menu')  # 메뉴로 리다이렉트
    else:
        form = EquipmentForm()  # GET 요청의 경우 빈 폼 생성

    return render(request, 'myapp/create_equipment.html', {'form': form})

def equipment_list_edit_mode(request):
    equipments = Equipment.objects.all()
    return render(request, 'myapp/equipment_list_edit.html', {'equipments': equipments})

def health_check(request):
    return HttpResponse("OK", content_type="text/plain")

