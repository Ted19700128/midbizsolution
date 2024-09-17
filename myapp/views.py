from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import EquipmentForm
from .models import Equipment

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
    return render(request, 'myapp/equipment_menu.html')

def equipment_list(request):
    equipments = Equipment.objects.all()
    return render(request, 'myapp/equipment_list.html', {'equipments': equipments})

def equipment_list_edit_mode(request):
    equipments = Equipment.objects.all()
    return render(request, 'myapp/equipment_list_edit.html', {'equipments': equipments})

def delete_equipment(request):
    if request.method == 'POST':
        equipment_ids = request.POST.getlist('equipment_ids')
        if equipment_ids:
            if 'confirm' in request.POST:
                # '예' 버튼을 누른 경우 삭제
                Equipment.objects.filter(id__in=equipment_ids).delete()
                return redirect('equipment_list')
            elif 'cancel' in request.POST:
                # '아니오' 버튼을 누른 경우
                return redirect('equipment_list_edit_mode')
            else:
                # 삭제 확인 페이지 렌더링
                equipments = Equipment.objects.filter(id__in=equipment_ids)
                return render(request, 'myapp/delete_confirmation.html', {'equipments': equipments})
        else:
            return redirect('equipment_list_edit_mode')
    else:
        return redirect('equipment_list')

def create_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
    else:
        form = EquipmentForm()
    return render(request, 'myapp/create_equipment.html', {'form': form})

def health_check(request):
    return HttpResponse("OK", content_type="text/plain")

from django.contrib import messages

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