# Generated by Django 5.1.1 on 2024-09-29 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pemledger', '0002_remove_equipment_floor_remove_equipment_line_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='floor',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='equipment',
            name='line_name',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='equipment',
            name='plant_location',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='equipment',
            name='plant_name',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='equipment',
            name='process_name',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='equipment',
            name='process_number',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='equipment',
            name='supplier_name',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
