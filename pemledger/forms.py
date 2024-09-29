#!-- D:/web/midbizsolution/pemledger/forms.py

from django import forms
from .models import Equipment

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = [
            'supplier_name', 'plant_name', 'floor', 'line_name', 'process_number', 'process_name',
            'equipment_number', 'name', 'model_name', 'manufacturer', 'mfg_date', 'mfg_number', 'equipment_type', 'specs',
            'first_install', 'first_implement', 'current_operation_place', 'management_team', 'overhaul',
            'current_status'
        ]
        # widgets와 labels를 Meta 클래스 안에 정의
        widgets = {
            'supplier_name': forms.TextInput(attrs={'class': 'form-control'}),
            'plant_name': forms.TextInput(attrs={'class': 'form-control'}),
            'floor': forms.TextInput(attrs={'class': 'form-control'}),
            'line_name': forms.TextInput(attrs={'class': 'form-control'}),
            'process_number': forms.TextInput(attrs={'class': 'form-control'}),
            'process_name': forms.TextInput(attrs={'class': 'form-control'}),
            'equipment_number': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_name': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'mfg_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # 날짜 필드에 date 타입 추가
            'mfg_number': forms.TextInput(attrs={'class': 'form-control'}),
            'equipment_type': forms.TextInput(attrs={'class': 'form-control'}),
            'specs': forms.TextInput(attrs={'class': 'form-control'}),
            'first_install': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # 날짜 필드에 date 타입 추가
            'first_implement': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # 날짜 필드에 date 타입 추가
            'current_operation_place': forms.TextInput(attrs={'class': 'form-control'}),
            'management_team': forms.TextInput(attrs={'class': 'form-control'}),
            'overhaul': forms.TextInput(attrs={'class': 'form-control'}),  
            'current_status': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'supplier_name': '업체명',
            'plant_name': '공장명',
            'floor': '층',
            'line_name': '라인명',
            'process_number': '공정번호',
            'process_name': '공정명',
            'euipment_number': '설비번호',
            'name': '설비명',
            'model_name': '모델명',
            'manufacturer': '제조사',
            'mfg_date': '제조일자',
            'mfg_number': '제조번호',
            'equipment_type': '형식',
            'specs': '사양',
            'first_install': '최초설치',
            'first_implement': '최초양산',
            'current_operation_place': '현 운영장소',
            'management_team': '관리부서',
            'overhaul': '오버홀',
            'current_status': '상태',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 필수 입력이 아닌 필드에 대해 required 속성 비활성화
        self.fields['mfg_date'].required = False
        self.fields['equipment_type'].required = False
        self.fields['specs'].required = False
        self.fields['first_implement'].required = False
        self.fields['overhaul'].required = False
