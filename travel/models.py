from django.db import models
from accounts.models import User
import uuid
from shortuuid.django_fields import ShortUUIDField
from .fields import DurationField
from datetime import date
from django.utils import timezone
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
    description = models.TextField(default="")
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
    image = models.ImageField(upload_to='hotels/')
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    total_rooms = models.PositiveIntegerField()
    available_from = models.DateField(default=date.today())
    available_to = models.DateField(default=date.today())
    website = models.URLField(null=True,blank=True)
    wifi_available = models.BooleanField(default=False)
    parking_available = models.BooleanField(default=False)


    def __str__(self):
        return self.name

class Room(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name="rooms")
    room_type = models.CharField(max_length=100)
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    image = models.ImageField(upload_to='room_images/')
    bed_type = models.CharField(max_length=50)
    view = models.CharField(max_length=50)
    available_rooms = models.IntegerField(default=1)
    smoking_allowed = models.BooleanField(default=False)
    pet_friendly = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.hotel.name} - {self.room_type}'
    
    def save(self, *args, **kwargs):
        min_price_room = Room.objects.filter(hotel=self.hotel).order_by('price').first()
        if min_price_room.price >= self.price:
            self.hotel.price = self.price
            self.hotel.save()
        super().save(*args, **kwargs)
    
class HotelImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel_images/')


class HotelAmenity(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    additional_cost = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.ManyToManyField(Room,blank=True)

    class Meta:
        verbose_name_plural = 'Hotel Amenities'
    
    def __str__(self):
        return self.name

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
    origin_city = models.CharField(max_length=100,default="")
    destination_city = models.CharField(max_length=100,default="")
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    car_type = models.ForeignKey(CarType,on_delete=models.CASCADE)
    seats = models.PositiveIntegerField()
    transmission_type = models.CharField(max_length=50, choices=[('Automatic', 'Automatic'), ('Manual', 'Manual')],default="Automatic")
    fuel_type = models.CharField(max_length=50, choices=[('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('Electric', 'Electric')],default="Petrol")
    ac = models.BooleanField()
    bags = models.BooleanField()
    images = models.ImageField(upload_to='cars/')
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2)
    tax_type = models.CharField(max_length=20)
    total_cars = models.PositiveIntegerField()
    available_cars = models.PositiveIntegerField()
    available_till = models.DateField(default=date.today())

    def __str__(self):
        return f"{self.make} {self.model}"


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
    image = models.ImageField(upload_to='airline_image/',null=True,blank=True)

    def __str__(self):
        return self.name

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departures')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivals')
    name = models.CharField(max_length=255,default="")
    departure_time = models.DateField()
    arrival_time = models.DateField()
    image = models.ImageField(upload_to="flight_images/",default="")
    duration = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    amenities = models.ManyToManyField('FlightAmenity', blank=True)
    in_flight_meal = models.BooleanField(default=False)
    wifi_available = models.BooleanField(default=False)
    entertainment = models.CharField(max_length=100,null=True,blank=True)
    cabin_class = models.CharField(max_length=50, choices=[('Economy', 'Economy'), ('Business', 'Business'), ('First Class', 'First Class')])
    layover_airport = models.CharField(max_length=100, null=True, blank=True)
    layover_duration = models.DurationField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.airline.name} {self.flight_number} - {self.departure_airport} to {self.arrival_airport}"


class FlightAmenity(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    additional_cost = models.DecimalField(max_digits=10, decimal_places=2)
    flights = models.ManyToManyField(Flight, blank=True)
    inflight_wifi = models.BooleanField(default=False)
    priority_boarding = models.BooleanField(default=False)
    lounge_access = models.BooleanField(default=False)


class Bus(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    bus_number = models.CharField(max_length=20)
    bus_type = models.CharField(max_length=20)
    operator = models.CharField(max_length=50)
    departure_station = models.CharField(max_length=100)
    arrival_station = models.CharField(max_length=100)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    arrival_date = models.DateField()
    arrival_time = models.TimeField()
    duration = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    amenities = models.ManyToManyField('BusAmenity', blank=True)
    wifi_available = models.BooleanField(default=False)
    power_outlets_available = models.BooleanField(default=False)
    refreshments_served = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.operator} - {self.bus_number}"
    
    class Meta:
        verbose_name_plural = "Buses"

class BusAmenity(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    additional_cost = models.DecimalField(max_digits=10, decimal_places=2)
    buses = models.ManyToManyField(Bus, blank=True)
    onboard_entertainment = models.BooleanField(default=False)
    reclining_seats = models.BooleanField(default=False)
    restroom_onboard = models.BooleanField(default=False)

class Package(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='package_image/',blank=True)
    origin_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    flights = models.ManyToManyField('Flight',related_name='package_flights',blank=True)
    cars = models.ManyToManyField('Car',related_name='package_cars',blank=True)
    buses = models.ManyToManyField('Bus',related_name='package_buses',blank=True)
    hotels = models.ManyToManyField('Hotel',related_name='package_hotels',blank=True)
    activities = models.TextField()
    duration = models.CharField(max_length=100,null=True,blank=True)
    included_meals = models.CharField(max_length=100,null=True,blank=True)
    departure = models.DateField(default=date.today())
    with_flights = models.BooleanField(default=False)
    total_rooms = models.IntegerField(blank=True,null=True)
    
    def __str__(self):
        return self.name



class Offer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=100, default="")
    code = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to="offer_images/",blank=True)
    flights = models.ManyToManyField('Flight',related_name='offer_flights',blank=True)
    cars = models.ManyToManyField('Car',related_name='offer_cars',blank=True)
    buses = models.ManyToManyField('Bus',related_name='offer_buses',blank=True)
    hotels = models.ManyToManyField('Hotel',related_name='offer_hotels',blank=True)
    packages = models.ManyToManyField('Package',related_name='offer_packages',blank=True)
    description = models.TextField()
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.code

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    passenger = models.IntegerField(default=0)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    reservation_date = models.DateField(default=date.today)

    class Meta:
        abstract = True

class HotelReservation(Reservation):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    total_guests = models.IntegerField(default=0)
    check_in_date = models.DateField()
    check_out_date = models.DateField()

    passenger = None

    def __str__(self):
        return f"{self.user.email} - {self.hotel.name} - {self.room.room_type}"

class CarReservation(Reservation):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rental_start_date = models.DateField()
    rental_end_date = models.DateField()

    def __str__(self):
        return f"{self.user.email} - {self.car.name} - {self.passenger}"

class FlightReservation(Reservation):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    departure_on = models.DateField()

    def __str__(self):
        return f"{self.user.email} - {self.flight.name} - {self.passenger}"

class BusReservation(Reservation):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    departure_on = models.DateField()

    def __str__(self):
        return f"{self.user.email} - {self.bus.name} - {self.passenger}"

class PackageReservation(Reservation):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.package.name} - {self.passenger}"



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
    hotel = models.ForeignKey(HotelReservation,on_delete=models.CASCADE,blank=True,null=True)
    car = models.ForeignKey(CarReservation,on_delete=models.CASCADE,blank=True,null=True)
    flight = models.ForeignKey(FlightReservation,on_delete=models.CASCADE,blank=True,null=True)
    bus = models.ForeignKey(BusReservation,on_delete=models.CASCADE,blank=True,null=True)
    package = models.ForeignKey(PackageReservation,on_delete=models.CASCADE,blank=True,null=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    order_id = models.CharField(max_length=100,null=True,blank=True)
    payment_id = models.CharField(max_length=100,null=True,blank=True)
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS_CHOICES,default='pending')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    check_in_date = models.DateField(blank=True,null=True)
    check_out_date = models.DateField(blank=True,null=True)

    def __str__(self):
        return self.user.email
        
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=15)
    message = models.TextField()
    
    def __str__(self):
        return f"{self.name} - {self.email}"


class Forex(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=100,default="")
    email = models.EmailField(max_length=100,default="")
    location = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    quantity = models.IntegerField()
    purpose_of_visit = models.CharField(max_length=100)
    booking_currency_for = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    action = models.CharField(max_length=100,choices=(('buy','Buy'),('sell','Sell')),default='buy')
    
    def __str__(self):
        return f'{self.location} - {self.currency}'
    
