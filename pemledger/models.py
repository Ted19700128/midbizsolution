# D:/web/midbizsolution/pemledger/models.py

from django.db import models, transaction

class Equipment(models.Model):
    supplier_name = models.CharField(max_length=100, blank=True, null=True)
    plant_location = models.CharField(max_length=100, blank=True, null=True)
    plant_name = models.CharField(max_length=100, blank=True, null=True)
    floor = models.CharField(max_length=10, blank=True, null=True)
    line_name = models.CharField(max_length=100, blank=True, null=True)
    process_number = models.CharField(max_length=10, blank=True, null=True)
    process_name = models.CharField(max_length=100, blank=True, null=True)
    equipment_number = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=10)
    model_name = models.CharField(max_length=15)
    manufacturer = models.CharField(max_length=10)
    mfg_date = models.DateField(blank=True, null=True)
    mfg_number = models.CharField(max_length=10, blank=True, null=True)
    equipment_type = models.CharField(max_length=15, blank=True, null=True)
    specs = models.TextField(blank=True, null=True)
    first_install = models.DateField()
    first_implement = models.DateField(blank=True, null=True)
    current_operation_place = models.CharField(max_length=10)
    management_team = models.CharField(max_length=10)
    overhaul = models.CharField(max_length=10, blank=True, null=True)
    current_status = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        if not self.equipment_number:
            with transaction.atomic():
                last_equipment = Equipment.objects.select_for_update().order_by('id').last()
                if last_equipment:
                    last_number = int(last_equipment.equipment_number[2:])
                    new_number = f'PF{last_number + 1:03d}'
                else:
                    new_number = 'PF001'
                self.equipment_number = new_number

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.equipment_number} - {self.name}"
