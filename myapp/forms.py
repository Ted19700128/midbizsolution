#!-- D:/web/midbizsolution/myapp/forms.py

from django import forms
from .models import Equipment

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'
        fields = [
            'equipment_number', 'name', 'model_name', 'manufacturer', 'mfg_date', 'mfg_number', 'equipment_type', 'specs',
            'first_install', 'first_implement', 'current_operation_place', 'management_team', 'overhaul', 'current_status'
        ]
        # widgets와 labels를 Meta 클래스 안에 정의
        widgets = {
            'equipment_number': forms.TextInput(attrs={'class': 'form-control'}),
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
            'euipment_number': '설비번호',
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 필수 입력이 아닌 필드에 대해 required 속성 비활성화
        self.fields['mfg_date'].required = False
        self.fields['mfg_number'].required = False
        self.fields['equipment_type'].required = False
        self.fields['specs'].required = False
        self.fields['first_implement'].required = False
        self.fields['overhaul'].required = False
