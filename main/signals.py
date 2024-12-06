from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TravelSchedule, Seat

@receiver(post_save, sender=TravelSchedule)
def create_seats_for_schedule(sender, instance, created, **kwargs):
    """
    Signal to automatically create 12 seats for a new TravelSchedule.
    """
    if created:  # Only add seats when the schedule is first created
        seats_to_create = []
        for i in range(1, 13):  # Generate seats 1 to 12
            seat = Seat(
                bus_schedule=instance,
                seat_number=str(i),  # Sequential seat numbers
                is_reserved=False,
                bus=instance.bus  # Associate the seat with the bus
            )
            seats_to_create.append(seat)
        
        # Bulk create the seats to optimize database writes
        Seat.objects.bulk_create(seats_to_create)
        print(f"12 seats added for the travel schedule: {instance}")
