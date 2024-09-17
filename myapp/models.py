# myapp/models.py

from django.db import models

class Equipment(models.Model):
    equipment_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    specs = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.equipment_number:
            last_equipment = Equipment.objects.order_by('id').last()
            if last_equipment:
                last_number = int(last_equipment.equipment_number[2:])
                new_number = f'PF{last_number + 1:03d}'
            else:
                new_number = 'PF001'
            self.equipment_number = new_number
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.equipment_number} - {self.name}"

