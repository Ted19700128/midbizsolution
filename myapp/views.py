from django.shortcuts import render, redirect
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
