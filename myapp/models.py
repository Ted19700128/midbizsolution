from django.db import models, transaction

class Equipment(models.Model):
    equipment_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    mfg_date = models.CharField(max_length=255)
    mfg_number = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=255)
    specs = models.CharField(max_length=255)

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
