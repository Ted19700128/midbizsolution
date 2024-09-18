#!-- D:/web/midbizsolution/myapp/forms.py

from django import forms
from .models import Equipment

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['equipment_number', 'name', 'model_name', 'manufacturer', 'mfg_date', 'mfg_number', 'equipment_type', 'specs']
        widgets = {
            'equipment_number': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_name': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'mfg_date': forms.TextInput(attrs={'class': 'form-control'}),
            'mfg_number': forms.TextInput(attrs={'class': 'form-control'}),
            'equipment_type': forms.TextInput(attrs={'class': 'form-control'}),
            'specs': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        labels = {
            'equipment_number': '설비 번호',
            'name': '설비 이름',
            'model_name': '모델명',
            'manufacturer': '제조사',
            'mfg_date': '제조 일자',
            'mfg_number': '제조 번호',
            'equipment_type': '형식',
            'specs': '사양',
        }


    def as_custom(self, exclude_fields=None):
        if exclude_fields is None:
            exclude_fields = []
        output = []
        for field in self:
            if field.name not in exclude_fields:
                output.append(f'<div class="form-group">{field.label_tag()} {field} {field} {field.errors}</div>')
        return '\n'.join(output)
