# plantlayout/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Plant, Unit, Line, Equipment
from .forms import CreatePlayoutForm, AddPlayoutForm, UpdatePlayoutForm, SearchPlayoutForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def playout_main(request):
    # 레이아웃 작성 이력 가져오기
    history = Plant.objects.all().order_by('-id')

    # 레이아웃 데이터 직렬화
    plants = Plant.objects.all()
    layout_data = serialize_layout_data(plants)

    context = {
        'history': history,
        'layout_data': layout_data,
    }
    return render(request, 'plantlayout/playout_main.html', context)

def create_playout(request):
    if request.method == 'POST':
        form = CreatePlayoutForm(request.POST)
        if form.is_valid():
            # 데이터 저장 로직
            plant = Plant.objects.create(
                name=form.cleaned_data['plant_name'],
                width=form.cleaned_data['plant_width'],
                length=form.cleaned_data['plant_length'],
                floor=form.cleaned_data['floor']
            )

            unit = Unit.objects.create(
                plant=plant,
                name=form.cleaned_data['unit_name'],
                start_point_x=form.cleaned_data['unit_start_point_x'],
                start_point_y=form.cleaned_data['unit_start_point_y'],
                end_point_x=form.cleaned_data['unit_end_point_x'],
                end_point_y=form.cleaned_data['unit_end_point_y']
            )

            line = Line.objects.create(
                unit=unit,
                name=form.cleaned_data['line_name'],
                start_point_x=form.cleaned_data['line_start_point_x'],
                start_point_y=form.cleaned_data['line_start_point_y'],
                end_point_x=form.cleaned_data['line_end_point_x'],
                end_point_y=form.cleaned_data['line_end_point_y']
            )

            equipment = Equipment.objects.create(
                line=line,
                process_number=form.cleaned_data['process_number'],
                position_x=form.cleaned_data['equipment_position_x'],
                position_y=form.cleaned_data['equipment_position_y'],
                size_width=form.cleaned_data['equipment_size_width'],
                size_length=form.cleaned_data['equipment_size_length']
            )

            messages.success(request, '공장 레이아웃이 생성되었습니다.')
            return redirect('plantlayout:playout_main')
    else:
        form = CreatePlayoutForm()
    return render(request, 'plantlayout/create_playout.html', {'form': form})

def add_playout(request):
    if request.method == 'POST':
        form = AddPlayoutForm(request.POST)
        if form.is_valid():
            # 데이터 저장 로직
            plant_id = form.cleaned_data['plant']
            plant = get_object_or_404(Plant, id=plant_id)

            # 필요한 데이터 저장 (예시로 Unit 추가)
            unit = Unit.objects.create(
                plant=plant,
                name=form.cleaned_data['unit_name'],
                start_point_x=form.cleaned_data['unit_start_point_x'],
                start_point_y=form.cleaned_data['unit_start_point_y'],
                end_point_x=form.cleaned_data['unit_end_point_x'],
                end_point_y=form.cleaned_data['unit_end_point_y']
            )

            # 전체 레이아웃 데이터 직렬화
            plants = Plant.objects.all()
            layout_data = serialize_layout_data(plants)

            return JsonResponse({'status': 'success', 'layoutData': layout_data})
        else:
            return JsonResponse({'status': 'error', 'message': '유효하지 않은 폼 데이터입니다.'})
    else:
        form = AddPlayoutForm()
    return render(request, 'plantlayout/add_playout.html', {'form': form})

def update_playout(request, equipment_id=None):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    if request.method == 'POST':
        form = UpdatePlayoutForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, '레이아웃이 변경되었습니다.')
            return redirect('plantlayout:playout_main')
    else:
        form = UpdatePlayoutForm(instance=equipment)
    return render(request, 'plantlayout/update_playout.html', {'form': form})

def search_playout(request):
    if request.method == 'GET':
        form = SearchPlayoutForm(request.GET)
        if form.is_valid():
            # 검색 로직
            equipments = Equipment.objects.all()
            if form.cleaned_data['plant_name']:
                equipments = equipments.filter(line__unit__plant__name=form.cleaned_data['plant_name'])
            if form.cleaned_data['floor']:
                equipments = equipments.filter(line__unit__plant__floor=form.cleaned_data['floor'])
            if form.cleaned_data['unit_name']:
                equipments = equipments.filter(line__unit__name=form.cleaned_data['unit_name'])
            if form.cleaned_data['line_name']:
                equipments = equipments.filter(line__name=form.cleaned_data['line_name'])
            if form.cleaned_data['equipment_number']:
                equipments = equipments.filter(equipment_number=form.cleaned_data['equipment_number'])

            return render(request, 'plantlayout/search_results.html', {'equipments': equipments})
    else:
        form = SearchPlayoutForm()
    return render(request, 'plantlayout/search_playout.html', {'form': form})

@csrf_exempt
def update_equipment_position(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        equipment_id = data.get('equipment_id')
        new_x = data.get('new_x')
        new_y = data.get('new_y')

        equipment = get_object_or_404(Equipment, id=equipment_id)
        equipment.position_x = new_x
        equipment.position_y = new_y
        equipment.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})

# 레이아웃 데이터를 직렬화하는 함수
def serialize_layout_data(plants):
    layout_data = {'plants': []}
    for plant in plants:
        plant_dict = {
            'name': plant.name,
            'floor': plant.floor,
            'width': plant.width,
            'length': plant.length,
            'units': []
        }
        units = Unit.objects.filter(plant=plant)
        for unit in units:
            unit_dict = {
                'name': unit.name,
                'start_point': {'x': unit.start_point_x, 'y': unit.start_point_y},
                'end_point': {'x': unit.end_point_x, 'y': unit.end_point_y},
                'lines': []
            }
            lines = Line.objects.filter(unit=unit)
            for line in lines:
                line_dict = {
                    'name': line.name,
                    'start_point': {'x': line.start_point_x, 'y': line.start_point_y},
                    'end_point': {'x': line.end_point_x, 'y': line.end_point_y},
                    'equipments': []
                }
                equipments = Equipment.objects.filter(line=line)
                for equipment in equipments:
                    equipment_dict = {
                        'id': equipment.id,
                        'equipment_number': equipment.equipment_number,
                        'position': {'x': equipment.position_x, 'y': equipment.position_y},
                        'size_width': equipment.size_width,
                        'size_length': equipment.size_length
                    }
                    line_dict['equipments'].append(equipment_dict)
                unit_dict['lines'].append(line_dict)
            plant_dict['units'].append(unit_dict)
        layout_data['plants'].append(plant_dict)
    return layout_data
