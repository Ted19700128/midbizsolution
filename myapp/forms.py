#!-- D:/web/midbizsolution/myapp/forms.py

from django import forms
from .models import Equipment

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['equipment_number', 'name', 'model_name', 'manufacturer', 'mfg_date', 'mfg_number', 'equipment_type', 'specs',
                  'first_install', 'first_implement', 'current_operation_place', 'management_team', 'overall', 'current_status']
        widgets = {
            'equipment_number': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_name': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'mfg_date': forms.TextInput(attrs={'class': 'form-control'}),
            'mfg_number': forms.TextInput(attrs={'class': 'form-control'}),
            'equipment_type': forms.TextInput(attrs={'class': 'form-control'}),
            'specs': forms.TextInput(attrs={'class': 'form-control'}),
            'first_install': forms.TextInput(attrs={'class': 'form-control'}),
            'first_implement': forms.TextInput(attrs={'class': 'form-control'}),
            'current_operation_place': forms.TextInput(attrs={'class': 'form-control'}),
            'management_team': forms.TextInput(attrs={'class': 'form-control'}),
            'overall': forms.TextInput(attrs={'class': 'form-control'}),
            'current_status': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'equipment_number': '설비번호',
            'name': '설비명',
            'model_name': '모델명',
            'manufacturer': '제조사',
            'mfg_date': '제조일자',
            'mfg_number': '제조번호',
            'equipment_type': '형식',
            'specs': '사양',
            'first_install': '최초설치시점',
            'first_implement': '최초양산적용',
            'current_operation_place': '현 운영장소',
            'management_team': '관리부서',
            'overhaul': '오버홀',
            'current_status': '상태',
        }


    def as_custom(self, exclude_fields=None):
        if exclude_fields is None:
            exclude_fields = []
        output = []
        for field in self:
            if field.name not in exclude_fields:
                output.append(f'<div class="form-group">{field.label_tag()} {field} {field} {field.errors}</div>')
        return '\n'.join(output)
