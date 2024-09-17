# myapp/views.py

from io import BytesIO
import pandas as pd
from django.http import HttpResponse
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
    equipments = Equipment.objects.all()

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
            messages.success(request, "설비 정보가 성공적으로 수정되었습니다.")
            return redirect('equipment_menu')  # 수정 후 설비 목록 페이지로 리다이렉트
        else:
            messages.error(request, "입력한 정보에 오류가 있습니다. 다시 시도해주세요.")
    else:
        form = EquipmentForm(instance=equipment)

    return render(request, 'myapp/update_equipment.html', {'form': form})

def delete_equipment(request):
    if request.method == 'POST':
        equipment_ids = request.POST.getlist('equipment_ids')
        
        if not equipment_ids:
            messages.error(request, "삭제할 설비를 선택하세요.")
            return redirect('equipment_menu')
        
        Equipment.objects.filter(id__in=equipment_ids).delete()
        messages.success(request, "선택한 설비가 성공적으로 삭제되었습니다.")
        return redirect('equipment_menu')
    
    return redirect('equipment_menu')  # GET 요청 시 기본적으로 equipment_menu로 리디렉
        
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
        if form.is_valid():
            form.save()
            return redirect('equipment_menu')
    else:
        form = EquipmentForm()
    return render(request, 'myapp/create_equipment.html', {'form': form})

def equipment_list_edit_mode(request):
    equipments = Equipment.objects.all()
    return render(request, 'myapp/equipment_list_edit.html', {'equipments': equipments})

def health_check(request):
    return HttpResponse("OK", content_type="text/plain")

