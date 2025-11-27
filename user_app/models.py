from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    address = models.TextField()

    def __str__(self):
        return self.user.username


class Station(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    def __str__(self): return f"{self.code} - {self.name}"

class Train(models.Model):
    number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=150)
    from_station = models.ForeignKey(Station, related_name="trains_from", on_delete=models.CASCADE)
    to_station = models.ForeignKey(Station, related_name="trains_to", on_delete=models.CASCADE)
    total_seats = models.PositiveIntegerField(default=120)
    def __str__(self): return f"{self.number} {self.name}"

class Booking(models.Model):
    STATUS_CHOICES = [('CONFIRMED','Confirmed'), ('CANCELLED','Cancelled'), ('PENDING','Pending')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    travel_date = models.DateField()
    class_type = models.CharField(max_length=20, default='SL')  
    quota = models.CharField(max_length=20, default='GN') 
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    def __str__(self): return f"Booking {self.id} - {self.user.username}"

class Passenger(models.Model):
    booking = models.ForeignKey(Booking, related_name='passengers', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    GENDER_CHOICES = [('M','Male'),('F','Female'),('O','Other')]
    BERTH_CHOICES = [
        ('nothing', 'Nothing'),
        ('L', 'Lower'),
        ('M', 'Middle'),
        ('U', 'Upper'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    berth_preference = models.CharField(
        max_length=10,
        choices=BERTH_CHOICES,
        blank=True,
        default='nothing' 
    )
    def __str__(self): return f"{self.name} ({self.age})"

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    method = models.CharField(max_length=50) 
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid_at = models.DateTimeField(null=True, blank=True)
    transaction_id = models.CharField(max_length=200, blank=True)
    def __str__(self): return f"Payment {self.booking.id} - {self.amount}"


# Create your models here.
