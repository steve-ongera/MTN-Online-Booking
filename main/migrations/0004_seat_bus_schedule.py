# Generated by Django 5.1.2 on 2024-12-03 22:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_travelschedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='bus_schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.travelschedule'),
        ),
    ]