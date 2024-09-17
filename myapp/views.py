from django.shortcuts import render, redirect
from .forms import EquipmentForm
from .models import Equipment
from django.http import HttpResponse

def landing_page(request):
    return render(request, 'landing_page.html')  # 템플릿 경로에 맞게 수정

def equipment_list(request):
    equipments = Equipment.objects.all()
    return render(request, 'myapp/equipment_list.html', {'equipments': equipments})

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
