#!-- D:/web/midbizsolution/myapp/forms.py

from django import forms
from .models import Equipment

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['equipment_number', 'name', 'model_name', 'manufacturer', 'mfg_date', 'mfg_number', 'types', 'specs']
        widgets = {
            'equipment_number': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_name': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'mfg_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'month',  # 'type="month"'으로 HTML5의 월 선택 입력을 사용
                    'placeholder': 'YYYY-MM',  # 입력 가이드로 플레이스홀더 추가
                }
            ),
            'mfg_number': forms.TextInput(attrs={'class': 'form-control'}),
            'types': forms.TextInput(attrs={'class': 'form-control'}),
            'specs': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
