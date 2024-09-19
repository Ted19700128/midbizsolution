#!-- D:/web/midbizsolution/pfcstandard/forms.py

from django import forms
from .models import PFCS

class DocumentForm(forms.ModelForm):
    class Meta:
        model = PFCS
        fields = ['document_number', 'equipment_number', 'name', 'management_team', 'date_written', 'rating', 'insp_interval',
                  'order', 'insp_point', 'insp_item', 'insp_int_rating', 'insp_method', 'judge_criteria', 'actions_required' ]
        widgets = {
            'document_number': forms.TextInput(attrs={'class': 'form-control'}),
            'equipment_number': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'management_team': forms.TextInput(attrs={'class': 'form-control'}),
            'date_written': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.TextInput(attrs={'class': 'form-control'}),
            'insp_interval': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.TextInput(attrs={'class': 'form-control'}),
            'insp_point': forms.TextInput(attrs={'class': 'form-control'}),
            'insp_item': forms.Textarea(attrs={'class': 'form-control'}),
            'insp_int_rating': forms.Textarea(attrs={'class': 'form-control'}),
            'insp_method': forms.Textarea(attrs={'class': 'form-control'}),
            'judge_criteria': forms.Textarea(attrs={'class': 'form-control'}),
            'actions_required': forms.Textarea(attrs={'class': 'form-control'}),
        }

        labels = {
            'document_number': '문서 번호',
            'equipment_number': '설비 번호',
            'name': '설비명',
            'management_team': '관리부서',
            'date_written': '작성일자',
            'rating': '설비등급',
            'insp_interval': '점검주기',
            
            'order': '번호',
            'insp_point': '점검부위',
            'insp_item': '점검항목',
            'insp_int_rating': '등급별 점검주기',
            'insp_method': '정검방법',
            'judge_criteria': '판정기준',
            'actions_required': '필요 조치',
        }