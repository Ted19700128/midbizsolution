# plantlayout/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Plant, Unit, Line, Equipment
from .forms import (
    CreatePlayoutForm,
    AddPlayoutForm,
    UpdatePlayoutForm,
    SearchPlayoutForm,
    EditPlantForm,
    EditUnitForm,
    EditLineForm,
    EditEquipmentForm,
)
import json

def playout_main(request):
    # 레이아웃 작성 이력 가져오기
    history = Plant.objects.all().order_by('-id')

    # 레이아웃 데이터 직렬화
    plants = Plant.objects.all()
    layout_data = serialize_layout_data(plants)
    layout_data_json = json.dumps(layout_data)  # JSON 문자열로 직렬화

    context = {
        'history': history,
        'layout_data': layout_data_json,
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
            plant = form.cleaned_data['plant']

            # 필요한 데이터 저장 (예시로 Unit 추가)
            unit = Unit.objects.create(
                plant=plant,
                name=form.cleaned_data['unit_name'],
                start_point_x=form.cleaned_data['unit_start_point_x'],
                start_point_y=form.cleaned_data['unit_start_point_y'],
                end_point_x=form.cleaned_data['unit_end_point_x'],
                end_point_y=form.cleaned_data['unit_end_point_y']
            )

            messages.success(request, '공장 레이아웃에 요소가 추가되었습니다.')
            return redirect('plantlayout:playout_main')
        else:
            messages.error(request, '유효하지 않은 폼 데이터입니다.')
    else:
        form = AddPlayoutForm()
    return render(request, 'plantlayout/add_playout.html', {'form': form})

def edit_playout(request):
    # 기존 레이아웃이 있는지 확인
    plants = Plant.objects.all()
    if not plants.exists():
        messages.info(request, '기존에 생성된 레이아웃이 없습니다.')
        return redirect('plantlayout:playout_main')
    
    plant = plants.first()  # 여러 개의 공장이 있다면 선택할 수 있도록 수정 가능

    if request.method == 'POST':
        plant_form = EditPlantForm(request.POST, instance=plant)
        if plant_form.is_valid():
            plant_form.save()
            messages.success(request, '공장 정보가 수정되었습니다.')
            return redirect('plantlayout:edit_playout')
    else:
        plant_form = EditPlantForm(instance=plant)
    
    # 관련된 Unit 정보를 가져옵니다.
    units = Unit.objects.filter(plant=plant)
    unit_forms = [EditUnitForm(instance=unit, prefix=f'unit_{unit.id}') for unit in units]

    context = {
        'plant_form': plant_form,
        'units': units,
        'unit_forms': unit_forms,
    }
    return render(request, 'plantlayout/edit_playout.html', context)

def edit_unit(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    if request.method == 'POST':
        unit_form = EditUnitForm(request.POST, instance=unit)
        if unit_form.is_valid():
            unit_form.save()
            messages.success(request, '구역 정보가 수정되었습니다.')
            return redirect('plantlayout:edit_playout')
    else:
        unit_form = EditUnitForm(instance=unit)
    return render(request, 'plantlayout/edit_unit.html', {'unit_form': unit_form})

def edit_line(request, line_id):
    line = get_object_or_404(Line, id=line_id)
    if request.method == 'POST':
        line_form = EditLineForm(request.POST, instance=line)
        if line_form.is_valid():
            line_form.save()
            messages.success(request, '라인 정보가 수정되었습니다.')
            return redirect('plantlayout:edit_playout')
    else:
        line_form = EditLineForm(instance=line)
    return render(request, 'plantlayout/edit_line.html', {'line_form': line_form})

def edit_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    if request.method == 'POST':
        equipment_form = EditEquipmentForm(request.POST, instance=equipment)
        if equipment_form.is_valid():
            equipment_form.save()
            messages.success(request, '설비 정보가 수정되었습니다.')
            return redirect('plantlayout:edit_playout')
    else:
        equipment_form = EditEquipmentForm(instance=equipment)
    return render(request, 'plantlayout/edit_equipment.html', {'equipment_form': equipment_form})

def update_playout(request, equipment_id=None):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    if request.method == 'POST':
        form = UpdatePlayoutForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, '설비 정보가 변경되었습니다.')
            return redirect('plantlayout:playout_main')
    else:
        form = UpdatePlayoutForm(instance=equipment)
    return render(request, 'plantlayout/update_playout.html', {'form': form, 'equipment': equipment})

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
