# myapp/views.py

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Equipment
from .forms import EquipmentForm

def equipment_menu(request):
    equipments = Equipment.objects.all()
    context = {
        'equipments': equipments,
        'create_equipment': reverse('create_equipment'),
        'equipment_list_edit_mode': reverse('equipment_list_edit_mode'),
    }
    return render(request, 'myapp/equipment_menu.html', context)

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

    # 엑셀 파일로 변환
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response

# 기타 뷰 함수들

def create_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
    else:
        form = EquipmentForm()
    return render(request, 'myapp/create_equipment.html', {'form': form})

def equipment_list_edit_mode(request):
    equipments = Equipment.objects.all()
    return render(request, 'myapp/equipment_list_edit.html', {'equipments': equipments})

# 필요에 따라 다른 뷰 함수들도 포함될 수 있습니다.
