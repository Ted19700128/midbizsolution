from django.shortcuts import render, redirect
from .forms import EquipmentForm
from .models import Equipment
from django.http import HttpResponse

# 설비 생성 뷰
def create_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()  # 모델의 save 메서드에서 설비 번호 자동 생성
            return redirect('equipment_list')  # 생성 후 설비 목록 페이지로 리다이렉트
    else:
        form = EquipmentForm()
    return render(request, 'myapp/create_equipment.html', {'form': form})

# 설비 목록 조회 뷰
def equipment_list(request):
    equipments = Equipment.objects.all()  # 모든 설비를 조회
    return render(request, 'myapp/equipment_list.html', {'equipments': equipments})

def health_check(request):
    return HttpResponse("OK", content_type="text/plain")
