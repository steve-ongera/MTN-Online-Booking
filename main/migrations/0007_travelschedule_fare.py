# Generated by Django 5.1.2 on 2024-12-05 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_seat_unique_seat_per_bus'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelschedule',
            name='fare',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
