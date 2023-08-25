from django.db import models
from accounts.models import User
import uuid
from shortuuid.django_fields import ShortUUIDField
from .fields import DurationField

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
    image = models.ImageField(upload_to='hotels/')
    total_rooms = models.PositiveIntegerField()
    available_rooms = models.PositiveIntegerField()


    def __str__(self):
        return self.name
    
class HotelImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel_images/')


class HotelAmenity(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Hotel Amenities'
    
    def __str__(self):
        return self.name

class CarType(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    type = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.type

class FuelType(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    fuel = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.fuel}"

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
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    car_type = models.ForeignKey(CarType,on_delete=models.CASCADE)
    fuel_type = models.ForeignKey(FuelType,on_delete=models.CASCADE)
    seats = models.PositiveIntegerField()
    transmission = models.CharField(max_length=10)  # Auto or Manual
    ac = models.BooleanField()
    bags = models.BooleanField()
    images = models.ImageField(upload_to='cars/')
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2)
    tax_type = models.CharField(max_length=20)
    total_cars = models.PositiveIntegerField()
    available_cars = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class AdImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    image = models.ImageField(upload_to='ads/')


# Airports
class Airport(models.Model):
    code = models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Airline(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departures')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivals')
    name = models.CharField(max_length=255,default="")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    image = models.ImageField(upload_to="flight_images/",default="")
    duration = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.airline.name} {self.flight_number} - {self.departure_airport} to {self.arrival_airport}"



class Bus(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    bus_number = models.CharField(max_length=20)
    bus_type = models.CharField(max_length=20)
    operator = models.CharField(max_length=50)
    departure_city = models.CharField(max_length=50)
    departure_time = models.DateTimeField()
    arrival_city = models.CharField(max_length=50)
    arrival_time = models.DateTimeField()
    duration = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.operator} - {self.bus_number}"
    
    class Meta:
        verbose_name_plural = "Buses"

class Package(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    origin_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    flights = models.ManyToManyField('Flight',related_name='package_flights')
    cars = models.ManyToManyField('Car',related_name='package_cars')
    buses = models.ManyToManyField('Bus',related_name='package_buses')
    hotels = models.ManyToManyField('Hotel',related_name='package_hotels')
    activities = models.TextField()
    duration = DurationField()

    def get_duration_days(self):
        return self.duration[0]

    def get_duration_nights(self):
        return self.duration[1]

    def set_duration(self, days, nights):
        self.duration = (days, nights)

class PackageImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    package = models.ForeignKey(Package,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='package_images/')

    def __str__(self):
        return f"Images for {self.package.name}"


class Offer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.code


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
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,blank=True,null=True)
    car = models.ForeignKey(Car,on_delete=models.CASCADE,blank=True,null=True)
    flight = models.ForeignKey(Flight,on_delete=models.CASCADE,blank=True,null=True)
    bus = models.ForeignKey(Bus,on_delete=models.CASCADE,blank=True,null=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    payment_id = models.CharField(max_length=100,null=True,blank=True)
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS_CHOICES,default='pending')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    check_in_date = models.DateField(blank=True,null=True)
    check_out_date = models.DateField(blank=True,null=True)

    def __str__(self):
        return self.user.email