# Generated by Django 5.1.2 on 2024-12-06 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_destination_fare'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_order_id',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True),
        ),
        migrations.DeleteModel(
            name='SeatBooking',
        ),
    ]
