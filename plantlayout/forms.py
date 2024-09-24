# plantlayout/forms.py

from django import forms
from .models import Plant, Unit, Line, Equipment

class CreatePlayoutForm(forms.Form):
    # 1행
    plant_name = forms.CharField(label='공장명')
    plant_width = forms.FloatField(label='공장 가로 길이')
    plant_length = forms.FloatField(label='공장 세로 길이')
    floor = forms.IntegerField(label='층')
    # 2행
    unit_name = forms.CharField(label='구역명')
    unit_start_point_x = forms.FloatField(label='구역 시작점 X')
    unit_start_point_y = forms.FloatField(label='구역 시작점 Y')
    unit_end_point_x = forms.FloatField(label='구역 끝점 X')
    unit_end_point_y = forms.FloatField(label='구역 끝점 Y')
    # 3행
    line_name = forms.CharField(label='라인명')
    line_start_point_x = forms.FloatField(label='라인 시작점 X')
    line_start_point_y = forms.FloatField(label='라인 시작점 Y')
    line_end_point_x = forms.FloatField(label='라인 끝점 X')
    line_end_point_y = forms.FloatField(label='라인 끝점 Y')
    # 4행
    process_number = forms.CharField(label='공정번호')
    # 5행
    equipment_position_x = forms.FloatField(label='설비 위치 X')
    equipment_position_y = forms.FloatField(label='설비 위치 Y')
    equipment_size_width = forms.FloatField(label='설비 가로 길이')
    equipment_size_length = forms.FloatField(label='설비 세로 길이')

class AddPlayoutForm(forms.Form):
    plant = forms.ModelChoiceField(queryset=Plant.objects.all(), label='공장 선택')
    unit_name = forms.CharField(label='구역명', required=False)
    unit_start_point_x = forms.FloatField(label='구역 시작점 X', required=False)
    unit_start_point_y = forms.FloatField(label='구역 시작점 Y', required=False)
    unit_end_point_x = forms.FloatField(label='구역 끝점 X', required=False)
    unit_end_point_y = forms.FloatField(label='구역 끝점 Y', required=False)
    # 추가로 Line과 Equipment 필드도 필요하면 추가

class UpdatePlayoutForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['position_x', 'position_y', 'size_width', 'size_length']  # equipment_number는 제외

class SearchPlayoutForm(forms.Form):
    plant_name = forms.CharField(label='공장명', required=False)
    floor = forms.IntegerField(label='층', required=False)
    unit_name = forms.CharField(label='구역명', required=False)
    line_name = forms.CharField(label='라인명', required=False)
    equipment_number = forms.CharField(label='설비번호', required=False)
