# Generated by Django 5.1.1 on 2024-09-21 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PFCS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_number', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('equipment_number', models.CharField(max_length=15, unique=True)),
                ('name', models.CharField(max_length=15)),
                ('management_team', models.CharField(max_length=15)),
                ('date_written', models.CharField(max_length=15)),
                ('rating', models.CharField(max_length=15)),
                ('insp_interval', models.CharField(max_length=50)),
                ('order', models.IntegerField()),
                ('insp_point', models.CharField(max_length=20)),
                ('insp_item', models.CharField(max_length=20)),
                ('insp_int_rating', models.CharField(max_length=10)),
                ('insp_method', models.CharField(max_length=50)),
                ('judge_criteria', models.CharField(max_length=50)),
                ('actions_required', models.CharField(max_length=20)),
            ],
        ),
    ]
