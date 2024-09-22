#!-- D:/web/midbizsolution/myapp/models.py

from django.db import models, transaction

class Equipment(models.Model):
    equipment_number = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=10)
    model_name = models.CharField(max_length=15)
    manufacturer = models.CharField(max_length=10)
    mfg_date = models.DateField(blank=True, null=True)  # 필수 입력이 아닌 경우
    mfg_number = models.CharField(max_length=10, blank=True, null=True)  # 필수 입력이 아닌 경우
    equipment_type = models.CharField(max_length=15, blank=True, null=True)
    specs = models.TextField(blank=True, null=True)
    first_install = models.DateField()
    first_implement = models.DateField(blank=True, null=True)
    current_operation_place = models.CharField(max_length=10)
    management_team = models.CharField(max_length=10)
    overhaul = models.CharField(max_length=10, blank=True, null=True)
    current_status = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        # 장비 번호가 없는 경우 새로 생성
        if not self.equipment_number:
            with transaction.atomic():  # 트랜잭션으로 묶어 동시성 문제 방지
                last_equipment = Equipment.objects.select_for_update().order_by('id').last()
                if last_equipment:
                    # 기존 장비 번호에서 숫자 부분을 추출하여 새 번호 생성
                    last_number = int(last_equipment.equipment_number[2:])
                    new_number = f'PF{last_number + 1:03d}'
                else:
                    new_number = 'PF001'
                self.equipment_number = new_number

        super().save(*args, **kwargs)  # 부모 클래스의 save() 메서드 호출하여 저장

    def __str__(self):
        return f"{self.equipment_number} - {self.name}"

#!-- 0922 추가 ============================================================   
class ManagementTeam(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
