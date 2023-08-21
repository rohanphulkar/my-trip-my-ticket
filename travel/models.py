from django.db import models
from accounts.models import User
import uuid
from shortuuid.django_fields import ShortUUIDField

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
    total_slots = models.PositiveIntegerField()
    available_slots = models.PositiveIntegerField()


    def __str__(self):
        return self.title

class TourImage(models.Model):
    tour = models.ForeignKey(Tour,on_delete=models.CASCADE,related_name='tour_images')
    image = models.ImageField(upload_to='tour_images/')

    def __str__(self):
        return f"Image for {self.tour.title}"


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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='hotels/')
    total_rooms = models.PositiveIntegerField()
    available_rooms = models.PositiveIntegerField()


    def __str__(self):
        return self.name
    
class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name='hotel_images')
    image = models.ImageField(upload_to='hotel_images/')

    def __str__(self):
        return f"Image for {self.hotel.name}"

class HotelAmenity(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Hotel Amenities'

class CarType(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    type = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.type

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
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    total_cars = models.PositiveIntegerField()
    available_cars = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class CarImage(models.Model):
    car = models.ForeignKey(Car,on_delete=models.CASCADE,related_name='car_images')
    image = models.ImageField(upload_to='car_images/')

    def __str__(self):
        return f"Image for {self.car.model}"

class AdImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    image = models.ImageField(upload_to='tour_ads/')


class UserItinerary(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    class Meta:
        verbose_name_plural = 'User Itineraries'


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending','Pending'),
        ('confirmed','Confirmed'),
        ('cancelled','Cancelled'),
        ('failed','Failed')
    )
    PAYMENT_STATUS_CHOICES = (
        ('pending','Pending'),
        ('paid','Paid'),
        ('failed','Failed')
    )
    id = ShortUUIDField(alphabet="0123456789",primary_key=True,length=8,max_length=10)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour,on_delete=models.CASCADE,blank=True,null=True)
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,blank=True,null=True)
    car = models.ForeignKey(Car,on_delete=models.CASCADE,blank=True,null=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    payment_id = models.CharField(max_length=100,null=True,blank=True)
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS_CHOICES,default='pending')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    check_in_date = models.DateField(blank=True,null=True)
    check_out_date = models.DateField(blank=True,null=True)

    def __str__(self):
        return self.user.email