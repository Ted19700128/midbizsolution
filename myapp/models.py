from django.db import models

class Equipment(models.Model):
    equipment_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    specs = models.TextField()

    def save(self, *args, **kwargs):
        if not self.equipment_number:
            last_equipment = Equipment.objects.all().order_by('id').last()
            if last_equipment:
                new_number = int(last_equipment.equipment_number[2:]) + 1
                self.equipment_number = f'PF{str(new_number).zfill(3)}'
            else:
                self.equipment_number = 'PF001'
        super().save(*args, **kwargs)
