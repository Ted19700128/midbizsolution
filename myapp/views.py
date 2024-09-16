from django.shortcuts import render, redirect
from .forms import EquipmentForm
from .models import Equipment

# 설비 생성 뷰
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

            return redirect('equipment_list')  # 생성 후 설비 목록 페이지로 리다이렉트
    else:
        form = EquipmentForm()
    
    return render(request, 'myapp/create_equipment.html', {'form': form})

# 설비 목록 조회 뷰
def equipment_list(request):
    equipments = Equipment.objects.all()  # 모든 설비를 조회
    return render(request, 'myapp/equipment_list.html', {'equipments': equipments})

from django.http import HttpResponse

def health_check(request):
    return HttpResponse("OK", content_type="text/plain")