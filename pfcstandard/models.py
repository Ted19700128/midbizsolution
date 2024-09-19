#!-- D:/web/midbizsolution/pfcstandard/models.py

from django.db import models, transaction

class PFCS(models.Model):
    document_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    equipment_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=15)
    management_team  = models.CharField(max_length=15)
    date_written  = models.CharField(max_length=15)
    rating  = models.CharField(max_length=15)
    insp_interval = models.CharField(max_length=50)
    
    order = models.IntegerField()
    insp_point = models.CharField(max_length=20)
    insp_item = models.CharField(max_length=20)
    insp_int_rating = models.CharField(max_length=10)
    insp_method = models.CharField(max_length=50)
    judge_criteria = models.CharField(max_length=50)
    actions_required = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        # 문서 번호가 없는 경우 새로 생성
        if not self.document_number:
            with transaction.atomic():  # 트랜잭션으로 묶어 동시성 문제 방지
                last_document = PFCS.objects.select_for_update().order_by('id').last()
                if last_document and last_document.document_number.startswith('SD-PF01-00-'):
                    # 기존 문서 번호에서 숫자 부분을 추출하여 새 번호 생성
                    last_number = int(last_document.document_number.split('-')[-1])
                    new_number = f'SD-PF01-00-{last_number + 1:03d}'
                else:
                    new_number = 'SD-PF01-00-001'
                self.document_number = new_number

        super().save(*args, **kwargs)  # 부모 클래스의 save() 메서드 호출하여 저장

    def __str__(self):
        return f"{self.document_number} - {self.name}"
