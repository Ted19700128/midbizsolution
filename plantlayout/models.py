# plantlayout/models.py

from django.db import models

class Plant(models.Model):
    name = models.CharField(max_length=10)
    width = models.FloatField()
    length = models.FloatField()
    floor = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Unit(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    start_point_x = models.FloatField()
    start_point_y = models.FloatField()
    end_point_x = models.FloatField()
    end_point_y = models.FloatField()

class Line(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    start_point_x = models.FloatField()
    start_point_y = models.FloatField()
    end_point_x = models.FloatField()
    end_point_y = models.FloatField()

class Equipment(models.Model):
    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    process_number = models.CharField(max_length=10)
    equipment_number = models.CharField(max_length=10, unique=True, blank=True)
    position_x = models.FloatField()
    position_y = models.FloatField()
    size_width = models.FloatField()
    size_length = models.FloatField()

    def save(self, *args, **kwargs):
        if not self.equipment_number:
            last_equipment = Equipment.objects.all().order_by('id').last()
            if last_equipment and last_equipment.equipment_number.startswith('PF'):
                last_number = int(last_equipment.equipment_number[2:])
                self.equipment_number = f'PF{last_number + 1:03d}'
            else:
                self.equipment_number = 'PF001'
        super().save(*args, **kwargs)