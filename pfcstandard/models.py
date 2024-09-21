#!-- D:/web/midbizsolution/pfcstandard/models.py

# models.py
from django.db import models, transaction

class PFCS(models.Model):
    document_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    equipment_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=50)  # 이름 필드 길이를 늘림
    management_team = models.CharField(max_length=50)  # 관리부서 길이를 늘림
    date_written = models.DateField(auto_now_add=True)  # 날짜 필드 자동 생성
    rating = models.CharField(max_length=2)  # 등급 필드 길이 조정
    insp_interval = models.CharField(max_length=1, choices=[('D', '일일'), ('W', '주간'), ('M', '월간'), ('Q', '분기'), ('H', '반기'), ('Y', '연간')])

    order = models.IntegerField()  # 자동 생성되는 순번
    insp_point = models.CharField(max_length=50)
    insp_item = models.CharField(max_length=100)
    insp_int_rating = models.CharField(max_length=10)
    insp_method = models.CharField(max_length=100)
    judge_criteria = models.CharField(max_length=100)
    actions_required = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.document_number:
            with transaction.atomic():
                last_document = PFCS.objects.select_for_update().order_by('id').last()
                if last_document and last_document.document_number.startswith('SD-PF01-00-'):
                    last_number = int(last_document.document_number.split('-')[-1])
                    new_number = f'SD-PF01-00-{last_number + 1:03d}'
                else:
                    new_number = 'SD-PF01-00-001'
                self.document_number = new_number

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.document_number} - {self.name}"
