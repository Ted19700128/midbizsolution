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
    show_table = mode in ['edit', 'view']
    equipments = Equipment.objects.all() if show_table else None
    context = {
        'create_equipment': reverse('create_equipment'),
        'equipment_list_edit_mode': reverse('equipment_list_edit_mode'),
        'show_table': show_table,
        'equipments': equipments,
        'mode': mode,
    }
    return render(request, 'myapp/equipment_menu.html', context)

def equipment_list(request):
    equipments = Equipment.objects.all()
    return render(request, 'myapp/equipment_list.html', {'equipments': equipments})

def update_equipment(request):
    if request.method == 'POST':
        equipment_ids = request.POST.getlist('equipment_ids')
        if not equipment_ids:
            messages.error(request, "변경할 설비를 선택하세요.")
            return redirect('equipment_list_edit_mode')
        elif len(equipment_ids) > 1:
            messages.error(request, "설비 정보 수정은 한 번에 한 설비에 대해서만 가능합니다. 한 설비만 선택해 주세요.")
            return redirect('equipment_list_edit_mode')
        else:
            equipment_id = equipment_ids[0]
            equipment = get_object_or_404(Equipment, id=equipment_id)
            if request.POST.get('confirm_update'):
                form = EquipmentForm(request.POST, instance=equipment)
                if form.is_valid():
                    form.save()
                    return redirect('equipment_list')
            else:
                form = EquipmentForm(instance=equipment)
            return render(request, 'myapp/update_equipment.html', {'form': form})
    else:
        return redirect('equipment_list')
    
def delete_equipment(request):
    if request.method == 'POST':
        equipment_ids = request.POST.getlist('equipment_ids')
        if equipment_ids:
            if 'confirm_delete' in request.POST:
                Equipment.objects.filter(id__in=equipment_ids).delete()
                messages.success(request, "선택한 설비가 삭제되었습니다.")
                return redirect('equipment_list')
            elif 'cancel_delete' in request.POST:
                messages.info(request, "삭제가 취소되었습니다.")
                return redirect('equipment_list')
            else:
                equipments = Equipment.objects.filter(id__in=equipment_ids)
                return render(request, 'myapp/delete_confirmation.html', {'equipments': equipments})
        else:
            messages.error(request, "삭제할 설비를 선택하세요.")
            return redirect('equipment_list_edit_mode')
    else:
        return redirect('equipment_list')

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
            return redirect('equipment_list')
    else:
        form = EquipmentForm()
    return render(request, 'myapp/create_equipment.html', {'form': form})

def equipment_list_edit_mode(request):
    equipments = Equipment.objects.all()
    return render(request, 'myapp/equipment_list_edit.html', {'equipments': equipments})

def health_check(request):
    return HttpResponse("OK", content_type="text/plain")

