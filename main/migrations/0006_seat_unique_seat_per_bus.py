# Generated by Django 5.1.2 on 2024-12-03 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_seat_seat_number'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='seat',
            constraint=models.UniqueConstraint(fields=('seat_number', 'bus'), name='unique_seat_per_bus'),
        ),
    ]
