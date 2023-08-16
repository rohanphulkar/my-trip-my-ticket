from django.db import models
from accounts.models import User
import uuid

class Tour(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    itinerary = models.TextField(verbose_name="tour_itinerary")
    activities = models.TextField()
    policies = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to='tours/')
    favorites = models.PositiveIntegerField(default=0)


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending','Pending'),
        ('confirmed','Confirmed'),
        ('cancelled','Cancelled')
    )
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour,on_delete=models.CASCADE)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    payment_status = models.BooleanField(default=False)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()



class Hotel(models.Model):
    STAR_CATEGORY_CHOICES = (
        (5, '5 Star'),
        (4, '4 Star'),
        (3, '3 Star'),
        (2, '2 Star'),
        (1, '1 Star'),
    )
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    name = models.CharField(max_length=200)
    address = models.TextField()
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pin = models.CharField(max_length=10)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    star_category = models.IntegerField(choices=STAR_CATEGORY_CHOICES)
    amenities = models.ManyToManyField('HotelAmenity', related_name='hotels')
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2)
    tax_type = models.CharField(max_length=20)  # Flat or Included in Rent
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='hotels/')

class HotelAmenity(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    name = models.CharField(max_length=50, unique=True)

class CarType(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    type = models.CharField(max_length=50, unique=True)

class Car(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    name = models.CharField(max_length=200)
    address = models.TextField()
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pin = models.CharField(max_length=10)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    car_type = models.ForeignKey(CarType,on_delete=models.CASCADE)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    passengers = models.PositiveIntegerField()
    transmission = models.CharField(max_length=10)  # Auto or Manual
    ac = models.BooleanField()
    bags = models.BooleanField()
    images = models.ImageField(upload_to='cars/')

class AdImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    image = models.ImageField(upload_to='tour_ads/')


class UserItinerary(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()