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
                    'type': 'month',
                    'placeholder': 'YYYY-MM',
                }
            ),
            'mfg_number': forms.TextInput(attrs={'class': 'form-control'}),
            'types': forms.TextInput(attrs={'class': 'form-control'}),
            'specs': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def as_custom(self):
        """
        Returns this form rendered as HTML <div>s for a custom layout,
        excluding the 'equipment_number' field.
        """
        output = []
        for field in self:
            if field.name != 'equipment_number':  # 'equipment_number' 필드를 제외
                output.append(f'<div class="form-group">{field.label_tag()} {field} {field.errors}</div>')
        return '\n'.join(output)