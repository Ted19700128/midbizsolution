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

def equipment_menu(request):
    mode = request.GET.get('mode')
    show_table = True
    equipments = Equipment.objects.all() if show_table else None
    context = {
        'create_equipment': reverse('create_equipment'),
        'equipment_list_edit_mode': reverse('equipment_list_edit_mode'),
        'mode': mode,
        'show_table': show_table,
        'equipments': equipments,
    }
    return render(request, 'myapp/equipment_menu.html', context)

def equipment_list(request):
    equipments = Equipment.objects.all()
    return render(request, 'myapp/equipment_list.html', {'equipments': equipments})

def update_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, "설비 정보가 성공적으로 수정되었습니다.")
            return redirect('equipment_menu')
        else:
            messages.error(request, "입력한 정보에 오류가 있습니다. 다시 시도해주세요.")
    else:
        form = EquipmentForm(instance=equipment)
    
    return render(request, 'myapp/update_equipment.html', {'form': form})
    
def delete_equipment(request):
    if request.method == 'POST':
        equipment_ids = request.POST.getlist('equipment_ids')
        if equipment_ids:
            if 'confirm_delete' in request.POST:
                Equipment.objects.filter(id__in=equipment_ids).delete()
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

