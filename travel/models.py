from django.db import models
from accounts.models import User
import uuid
from shortuuid.django_fields import ShortUUIDField
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
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
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
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_rooms = models.PositiveIntegerField()
    available_from = models.DateField(default=date.today())
    available_to = models.DateField(default=date.today())
    website = models.URLField(null=True, blank=True)
    wifi_available = models.BooleanField(default=False)
    parking_available = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Room(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="rooms")
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
        # Get the minimum price room for the hotel
        min_price_room = Room.objects.filter(
            hotel=self.hotel).order_by('price').first()

        if min_price_room is not None:
            if min_price_room.price >= self.price:
                # Update the hotel's price if the new room price is lower
                self.hotel.price = self.price
                self.hotel.save()
        else:
            self.hotel.price = self.price
            self.hotel.save()
        super().save(*args, **kwargs)


class HotelImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel_images/')


class HotelAmenity(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    additional_cost = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.ManyToManyField(Room, blank=True)

    class Meta:
        verbose_name_plural = 'Hotel Amenities'

    def __str__(self):
        return self.name


class CarType(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    type = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.type


class Car(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=200)
    address = models.TextField()
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pin = models.CharField(max_length=10)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    origin_city = models.CharField(max_length=100, default="")
    destination_city = models.CharField(max_length=100, default="")
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    seats = models.PositiveIntegerField()
    image = models.ImageField(upload_to='cars/')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2)
    tax_type = models.CharField(max_length=20)
    total_cars = models.PositiveIntegerField()
    available_cars = models.PositiveIntegerField()
    available_till = models.DateField(default=date.today())

    def __str__(self):
        return f"{self.make} {self.model}"


class CarImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='car_images/')

    def __str__(self):
        return f"{self.car.make} {self.car.model}"


# Airports
class Airport(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Airline(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='airline_image/', null=True, blank=True)

    def __str__(self):
        return self.name


class Flight(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    flight_number = models.CharField(max_length=10, unique=True)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    departure_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name='departures')
    arrival_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name='arrivals')
    name = models.CharField(max_length=255, default="")
    departure_time = models.DateField()
    arrival_time = models.DateField()
    image = models.ImageField(
        upload_to="flight_images/", default="")
    duration = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    amenities = models.ManyToManyField('FlightAmenity', blank=True)
    in_flight_meal = models.BooleanField(default=False)
    wifi_available = models.BooleanField(default=False)
    entertainment = models.CharField(max_length=100, null=True, blank=True)
    cabin_class = models.CharField(max_length=50, choices=[(
        'Economy', 'Economy'), ('Business', 'Business'), ('First Class', 'First Class')])
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

    def __str__(self):
        return self.name


class Bus(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    image = models.ImageField(upload_to='bus_images/',null=True,blank=True)
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

class BusImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    bus  = models.ForeignKey(Bus, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='bus_images/')

    def __str__(self):
        return f"{self.bus.name}"


class BusAmenity(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    additional_cost = models.DecimalField(max_digits=10, decimal_places=2)
    buses = models.ManyToManyField(Bus, blank=True)
    onboard_entertainment = models.BooleanField(default=False)
    reclining_seats = models.BooleanField(default=False)
    restroom_onboard = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Yacht(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    specifications = models.TextField(null=True, blank=True)
    layout = models.TextField(null=True, blank=True)
    crew_members = models.PositiveSmallIntegerField(null=True, blank=True)
    manufacturer = models.CharField(max_length=100, null=True, blank=True)
    year_built = models.PositiveSmallIntegerField(null=True, blank=True)
    maximum_speed = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)  # In knots
    fuel_capacity = models.PositiveIntegerField(
        null=True, blank=True)  # In liters
    cruising_range = models.CharField(
        max_length=100, null=True, blank=True)  # In nautical miles
    cabins = models.PositiveSmallIntegerField(default=0)
    bathrooms = models.PositiveSmallIntegerField(default=0)
    engine_power = models.CharField(max_length=100, null=True, blank=True)
    guest_capacity = models.PositiveSmallIntegerField(default=0)
    exterior_features = models.TextField(null=True, blank=True)
    interior_features = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='yacht_images/')
    registration_country = models.CharField(
        max_length=100, null=True, blank=True)
    hull_material = models.CharField(max_length=100, null=True, blank=True)
    length_overall = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)  # In meters
    draft = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)  # In meters
    beam = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)  # In meters
    owner = models.CharField(max_length=100, null=True, blank=True)
    charter_price = models.DecimalField(
        max_digits=10, decimal_places=2)  # Daily charter price
    description = models.TextField(null=True, blank=True)
    amenities = models.TextField(null=True, blank=True)
    special_features = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class YachtImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    yacht = models.ForeignKey(Yacht, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='yacht_images/')

    def __str__(self):
        return f"{self.yacht.name}"


class Activities(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(
        upload_to='activity_images/', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ThemePark(Activities):
    location = models.CharField(max_length=100)
    opening_date = models.DateField()
    website = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    capacity = models.PositiveIntegerField()
    parking_available = models.BooleanField(default=True)
    facilities = models.TextField(blank=True)


class ThemeParkImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    theme_park = models.ForeignKey(ThemePark, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='theme_park_images/')

    def __str__(self):
        return f"{self.theme_park.name}"


class TopAttraction(Activities):
    theme_park = models.ForeignKey(ThemePark, on_delete=models.CASCADE)
    thrill_level = models.PositiveIntegerField()
    age_limit = models.PositiveIntegerField()
    opening_hours = models.CharField(max_length=100)
    is_fast_pass_available = models.BooleanField(default=False)


class TopAttractionImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    top_attraction = models.ForeignKey(TopAttraction, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='top_attraction_images/')

    def __str__(self):
        return f"{self.top_attraction.name}"


class DesertSafari(Activities):
    location = models.CharField(max_length=100)
    duration_hours = models.PositiveIntegerField(blank=True, null=True)
    schedule = models.TextField(blank=True)
    inclusions = models.TextField(blank=True)
    max_participants = models.PositiveIntegerField()
    equipment_provided = models.TextField(blank=True)
    safety_guidelines = models.TextField(blank=True)


class DesertSafariImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    desert_safari = models.ForeignKey(DesertSafari, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='desert_safari_images/')

    def __str__(self):
        return f"{self.desert_safari.name}"


class WaterPark(Activities):
    location = models.CharField(max_length=100)
    opening_date = models.DateField()
    website = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    capacity = models.PositiveIntegerField()
    parking_available = models.BooleanField(default=True)
    facilities = models.TextField(blank=True)


class WaterParkImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    water_park = models.ForeignKey(WaterPark, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='water_park_images/')

    def __str__(self):
        return f"{self.water_park.name}"


class WaterActivity(Activities):
    water_park = models.ForeignKey(WaterPark, on_delete=models.CASCADE)
    age_limit = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    equipment_required = models.TextField(blank=True)
    skill_level = models.CharField(max_length=50)


class WaterActivityImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    water_activity = models.ForeignKey(WaterActivity, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='water_activity_images/')

    def __str__(self):
        return f"{self.water_activity.name}"


class AdventureTour(Activities):
    location = models.CharField(max_length=100)
    duration_days = models.PositiveIntegerField()
    itinerary = models.TextField(blank=True)
    max_participants = models.PositiveIntegerField()
    gear_provided = models.TextField(blank=True)
    difficulty_level = models.CharField(max_length=50)


class AdventureTourImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    adventure_tour = models.ForeignKey(AdventureTour, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='adventure_tour_images/')

    def __str__(self):
        return f"{self.adventure_tour.name}"


class ComboTour(Activities):
    theme_park = models.ForeignKey(ThemePark, on_delete=models.CASCADE)
    desert_safari = models.ForeignKey(DesertSafari, on_delete=models.CASCADE)
    water_park = models.ForeignKey(WaterPark, on_delete=models.CASCADE)
    adventure_tour = models.ForeignKey(AdventureTour, on_delete=models.CASCADE)
    duration_days = models.PositiveIntegerField()
    inclusion_details = models.TextField()
    reservation_instructions = models.TextField()
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)


class ComboTourImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    combo_tour = models.ForeignKey(ComboTour, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='combo_tour_images/')

    def __str__(self):
        return f"{self.combo_tour.name}"


class DubaiActivity(Activities):
    location = models.CharField(max_length=100)
    duration_hours = models.PositiveIntegerField()
    age_limit = models.PositiveIntegerField()
    includes_meals = models.BooleanField(default=False)
    schedule = models.TextField(blank=True)
    special_requirements = models.TextField(blank=True)
    max_participants = models.PositiveIntegerField()
    equipment_provided = models.TextField(blank=True)
    additional_info = models.TextField(blank=True)


class DubaiActivityImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    dubai_activity = models.ForeignKey(DubaiActivity, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='dubai_activity_images/')

    def __str__(self):
        return f"{self.dubai_activity.name}"


class CityTour(Activities):
    location = models.CharField(max_length=100)
    duration_hours = models.PositiveIntegerField()
    age_limit = models.PositiveIntegerField()
    includes_meals = models.BooleanField(default=False)
    schedule = models.TextField(blank=True)
    special_requirements = models.TextField(blank=True)
    max_participants = models.PositiveIntegerField()
    equipment_provided = models.TextField(blank=True)
    additional_info = models.TextField(blank=True)


class CityTourImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    city_tour = models.ForeignKey(CityTour, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='city_tour_images/')

    def __str__(self):
        return f"{self.city_tour.name}"


class Sightseeing(Activities):
    location = models.CharField(max_length=100)
    duration_hours = models.PositiveIntegerField(blank=True, null=True)
    landmarks = models.TextField(blank=True)
    guide_available = models.BooleanField(default=False)
    transportation_included = models.BooleanField(default=False)
    ticket_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    operating_season = models.CharField(max_length=100, blank=True)
    highlights = models.TextField(blank=True)
    inclusions = models.TextField(blank=True)


class SightseeingImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    sightseeing = models.ForeignKey(Sightseeing, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='sightseeing_images/')

    def __str__(self):
        return f"{self.sightseeing.name}"


class DhowCruiseDubai(Activities):
    location = models.CharField(max_length=100)
    duration_hours = models.PositiveIntegerField(blank=True, null=True)
    cruise_type = models.CharField(max_length=100, blank=True)
    entertainment_included = models.TextField(blank=True)
    dining_options = models.TextField(blank=True)
    capacity = models.PositiveIntegerField()
    reservations_required = models.BooleanField(default=False)
    departure_schedule = models.CharField(max_length=100, blank=True)
    special_events = models.TextField(blank=True)
    inclusions = models.TextField(blank=True)


class DhowCruiseDubaiImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    dhow_cruise_dubai = models.ForeignKey(
        DhowCruiseDubai, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='dhow_cruise_dubai_images/')

    def __str__(self):
        return f"{self.dhow_cruise_dubai.name}"


class GlampingTours(Activities):
    location = models.CharField(max_length=100)
    duration_nights = models.PositiveIntegerField(blank=True, null=True)
    accommodation_type = models.CharField(max_length=100, blank=True)
    activities_included = models.TextField(blank=True)
    camping_guide = models.BooleanField(default=False)
    all_inclusive = models.BooleanField(default=False)
    package_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    amenities = models.TextField(blank=True)
    restrictions = models.TextField(blank=True)
    inclusions = models.TextField(blank=True)


class GlampingToursImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    glamping_tours = models.ForeignKey(GlampingTours, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='glamping_tours_images/')

    def __str(self):
        return f"{self.glamping_tours.name}"


class BurjKhalifaTours(Activities):
    observation_deck = models.CharField(max_length=100)
    ticket_options = models.TextField(blank=True)
    guided_tours = models.TextField(blank=True)
    special_events = models.TextField(blank=True)
    height = models.PositiveIntegerField()
    booking_required = models.BooleanField(default=True)
    available_dates = models.CharField(max_length=100, blank=True)
    time_slots = models.TextField(blank=True)
    admission_fee = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    inclusions = models.TextField(blank=True)


class BurjKhalifaToursImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    burj_khalifa_tours = models.ForeignKey(
        BurjKhalifaTours, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='burj_khalifa_tours_images/')

    def __str__(self):
        return f"{self.burj_khalifa_tours.name}"


class SkyAdventures(Activities):
    location = models.CharField(max_length=100)
    adventure_type = models.CharField(max_length=100, blank=True)
    equipment_rental = models.TextField(blank=True)
    safety_guidelines = models.TextField(blank=True)
    weight_limit = models.PositiveIntegerField(blank=True, null=True)
    age_limit = models.PositiveIntegerField(blank=True, null=True)
    available_dates = models.CharField(max_length=100, blank=True)
    booking_options = models.TextField(blank=True)
    adrenaline_level = models.PositiveIntegerField(blank=True, null=True)
    group_size = models.PositiveIntegerField(blank=True, null=True)
    inclusions = models.TextField(blank=True)


class SkyAdventuresImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    sky_adventures = models.ForeignKey(SkyAdventures, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='sky_adventures_images/')

    def __str__(self):
        return f"{self.sky_adventures.name}"

class SeaAdventure(Activities):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    location = models.CharField(max_length=100)
    duration_hours = models.PositiveIntegerField(blank=True, null=True)
    adventure_type = models.CharField(max_length=100, blank=True)
    equipment_rental = models.TextField(blank=True)
    safety_guidelines = models.TextField(blank=True)
    weight_limit = models.PositiveIntegerField(blank=True, null=True)
    age_limit = models.PositiveIntegerField(blank=True, null=True)
    available_dates = models.CharField(max_length=100, blank=True)
    booking_options = models.TextField(blank=True)
    inclusions = models.TextField(blank=True)


class SeaAdventureImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    sea_adventure = models.ForeignKey(SeaAdventure, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='sea_adventure_images/')

    def __str__(self):
        return f"{self.sea_adventure.name}"




CATEGORIES = (
    ('top attraction', 'Top Attraction'),
    ('desert safari', 'Desert Safari'),
    ('water park', 'Water Park'),
    ('theme park', 'Theme Park'),
    ('water activity', 'Water Activity'),
    ('adventure tour', 'Adventure Tour'),
    ('combo tour', 'Combo Tour')
)


class Package(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to='package_image/', blank=True)
    origin_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORIES, default="")
    flights = models.ManyToManyField(
        'Flight', related_name='package_flights', blank=True)
    cars = models.ManyToManyField(
        'Car', related_name='package_cars', blank=True)
    buses = models.ManyToManyField(
        'Bus', related_name='package_buses', blank=True)
    hotels = models.ManyToManyField(
        'Hotel', related_name='package_hotels', blank=True)
    activities = models.TextField()
    duration = models.CharField(max_length=100, null=True, blank=True)
    included_meals = models.CharField(max_length=100, null=True, blank=True)
    departure = models.DateField(default=date.today())
    with_flights = models.BooleanField(default=False)
    total_rooms = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Offer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=100, default="")
    code = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to="offer_images/")
    flights = models.ManyToManyField(
        'Flight', related_name='offer_flights', blank=True)
    cars = models.ManyToManyField('Car', related_name='offer_cars', blank=True)
    buses = models.ManyToManyField(
        'Bus', related_name='offer_buses', blank=True)
    hotels = models.ManyToManyField(
        'Hotel', related_name='offer_hotels', blank=True)
    packages = models.ManyToManyField(
        'Package', related_name='offer_packages', blank=True)
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

    id = models.UUIDField(default=uuid.uuid4, editable=False,
                          primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    passenger = models.IntegerField(default=0)
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default='pending')
    reservation_date = models.DateField(default=date.today)

    class Meta:
        abstract = True


class HotelReservation(Reservation):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    total_guests = models.IntegerField(default=0)
    check_in_date = models.DateField(blank=True)
    check_out_date = models.DateField(blank=True)

    passenger = None

    def __str__(self):
        return f"{self.user.email} - {self.hotel.name} - {self.room.room_type}"


class CarReservation(Reservation):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rental_start_date = models.DateField()
    rental_end_date = models.DateField()

    def __str__(self):
        return f"{self.user.email} - {self.car.name} - {self.passenger}"


class YachtReservation(Reservation):
    yacht = models.ForeignKey(Yacht, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()

    def __str__(self):
        return f"{self.user.email} - {self.yacht.name} - {self.passenger}"


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


class ThemeParkReservation(Reservation):
    theme_park = models.ForeignKey(ThemePark, on_delete=models.CASCADE)
    admission_count = models.PositiveIntegerField()
    passenger = None

    def __str__(self):
        return f"{self.user.email} - {self.theme_park.name} - {self.admission_count} tickets"


class TopAttractionReservation(Reservation):
    top_attraction = models.ForeignKey(TopAttraction, on_delete=models.CASCADE)
    ticket_count = models.PositiveIntegerField()
    passenger = None

    def __str__(self):
        return f"{self.user.email} - {self.top_attraction.name} - {self.ticket_count} tickets"


class DesertSafariReservation(Reservation):
    desert_safari = models.ForeignKey(DesertSafari, on_delete=models.CASCADE)
    participant_count = models.PositiveIntegerField()
    passenger = None

    def __str__(self):
        return f"{self.user.email} - Desert Safari at {self.desert_safari.location} - {self.participant_count} participants"


class WaterParkReservation(Reservation):
    water_park = models.ForeignKey(WaterPark, on_delete=models.CASCADE)
    admission_count = models.PositiveIntegerField()
    passenger = None

    def __str__(self):
        return f"{self.user.email} - {self.water_park.name} - {self.admission_count} tickets"


class WaterActivityReservation(Reservation):
    water_activity = models.ForeignKey(WaterActivity, on_delete=models.CASCADE)
    participant_count = models.PositiveIntegerField()
    passenger = None

    def __str__(self):
        return f"{self.user.email} - {self.water_activity.name} - {self.participant_count} participants"


class AdventureTourReservation(Reservation):
    adventure_tour = models.ForeignKey(AdventureTour, on_delete=models.CASCADE)
    participant_count = models.PositiveIntegerField()
    passenger = None

    def __str__(self):
        return f"{self.user.email} - {self.adventure_tour.name} - {self.participant_count} participants"


class ComboTourReservation(Reservation):
    combo_tour = models.ForeignKey(ComboTour, on_delete=models.CASCADE)
    participant_count = models.PositiveIntegerField()
    passenger = None

    def __str__(self):
        return f"{self.user.email} - {self.combo_tour.name} - {self.participant_count} participants"


class DubaiActivityReservation(Reservation):
    dubai_activity = models.ForeignKey(DubaiActivity, on_delete=models.CASCADE)
    participant_count = models.PositiveIntegerField()
    passenger = None

    def __str__(self):
        return f"{self.user.email} - {self.dubai_activity.name} - {self.participant_count} participants"


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Failed')
    )
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed')
    )
    id = ShortUUIDField(alphabet="0123456789",
                        primary_key=True, length=8, max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(
        HotelReservation, on_delete=models.CASCADE, blank=True, null=True)
    car = models.ForeignKey(
        CarReservation, on_delete=models.CASCADE, blank=True, null=True)
    flight = models.ForeignKey(
        FlightReservation, on_delete=models.CASCADE, blank=True, null=True)
    bus = models.ForeignKey(
        BusReservation, on_delete=models.CASCADE, blank=True, null=True)
    package = models.ForeignKey(
        PackageReservation, on_delete=models.CASCADE, blank=True, null=True)
    yacht = models.ForeignKey(
        YachtReservation, on_delete=models.CASCADE, blank=True, null=True)
    theme_park = models.ForeignKey(
        ThemeParkReservation, on_delete=models.CASCADE, blank=True, null=True)
    top_attraction = models.ForeignKey(
        TopAttractionReservation, on_delete=models.CASCADE, blank=True, null=True)
    desert_safari = models.ForeignKey(
        DesertSafariReservation, on_delete=models.CASCADE, blank=True, null=True)
    water_park = models.ForeignKey(
        WaterParkReservation, on_delete=models.CASCADE, blank=True, null=True)
    water_activity = models.ForeignKey(
        WaterActivityReservation, on_delete=models.CASCADE, blank=True, null=True)
    adventure_tour = models.ForeignKey(
        AdventureTourReservation, on_delete=models.CASCADE, blank=True, null=True)
    combo_tour = models.ForeignKey(
        ComboTourReservation, on_delete=models.CASCADE, blank=True, null=True)
    dubai_activity = models.ForeignKey(
        DubaiActivityReservation, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to="pdf/", null=True, blank=True)
    check_in_date = models.DateField(blank=True, null=True)
    check_out_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.email}"


class Forex(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=100, default="")
    email = models.EmailField(max_length=100, default="")
    location = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    quantity = models.IntegerField()
    purpose_of_visit = models.CharField(max_length=100)
    booking_currency_for = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    action = models.CharField(max_length=100, choices=(
        ('buy', 'Buy'), ('sell', 'Sell')), default='buy')

    def __str__(self):
        return f'{self.location} - {self.currency}'


class Visa(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=100, default="")
    email = models.EmailField(max_length=100, default="")
    country = models.CharField(max_length=100)
    visa_type = models.CharField(max_length=100)
    traveller = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.email} - {self.visa_type} - {self.traveller}'


class RefundRequest(models.Model):
    REFUND_STATUS = (
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded')
    )
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(
        HotelReservation, on_delete=models.CASCADE, blank=True, null=True)
    car = models.ForeignKey(
        CarReservation, on_delete=models.CASCADE, blank=True, null=True)
    flight = models.ForeignKey(
        FlightReservation, on_delete=models.CASCADE, blank=True, null=True)
    bus = models.ForeignKey(
        BusReservation, on_delete=models.CASCADE, blank=True, null=True)
    package = models.ForeignKey(
        PackageReservation, on_delete=models.CASCADE, blank=True, null=True)
    yacht = models.ForeignKey(
        YachtReservation, on_delete=models.CASCADE, blank=True, null=True)
    theme_park = models.ForeignKey(
        ThemeParkReservation, on_delete=models.CASCADE, blank=True, null=True)
    top_attraction = models.ForeignKey(
        TopAttractionReservation, on_delete=models.CASCADE, blank=True, null=True)
    desert_safari = models.ForeignKey(
        DesertSafariReservation, on_delete=models.CASCADE, blank=True, null=True)
    water_park = models.ForeignKey(
        WaterParkReservation, on_delete=models.CASCADE, blank=True, null=True)
    water_activity = models.ForeignKey(
        WaterActivityReservation, on_delete=models.CASCADE, blank=True, null=True)
    adventure_tour = models.ForeignKey(
        AdventureTourReservation, on_delete=models.CASCADE, blank=True, null=True)
    combo_tour = models.ForeignKey(
        ComboTourReservation, on_delete=models.CASCADE, blank=True, null=True)
    dubai_activity = models.ForeignKey(
        DubaiActivityReservation, on_delete=models.CASCADE, blank=True, null=True)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=100, default='pending', choices=REFUND_STATUS)
    request_date = models.DateTimeField(auto_now_add=True)
    refund_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'refund request of {self.user.email}'


# Cutomer Review Models
class HotelCustomerReview(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    hotel = models.ForeignKey(
        'Hotel', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    review_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.hotel.name} by {self.user.email or self.user.phone}"


class CarCustomerReview(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    car = models.ForeignKey(
        'Car', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    review_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.car.name} by {self.user.email or self.user.phone}"


class FlightCustomerReview(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    flight = models.ForeignKey(
        'Flight', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    review_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.flight.flight_number} by {self.user.email or self.user.phone}"


class PackageCustomerReview(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    package = models.ForeignKey(
        'Package', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    review_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review for Package '{self.package.name}' by {self.user.email or self.user.phone}"


class YachtCustomerReview(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    yacht = models.ForeignKey(
        'Yacht', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    review_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.yacht.name} by {self.user.email or self.user.phone}"


class ThemeParkCustomerReview(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    themepark = models.ForeignKey(
        'ThemePark', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    review_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review for Theme Park '{self.themepark.name}' by {self.user.email or self.user.phone}"


class TopAttractionCustomerReview(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    topattraction = models.ForeignKey(
        'TopAttraction', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    review_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review for Top Attraction '{self.topattraction.name}' by {self.user.email or self.user.phone}"


class DesertSafariCustomerReview(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    desertsafari = models.ForeignKey(
        'DesertSafari', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    review_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review for Desert Safari '{self.desertsafari.name}' by {self.user.email or self.user.phone}"


class WaterParkCustomerReview(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    waterpark = models.ForeignKey(
        'WaterPark', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    review_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review for Water Park '{self.waterpark.name}' by {self.user.email or self.user.phone}"


class WaterActivityCustomerReview(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    wateractivity = models.ForeignKey(
        'WaterActivity', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    review_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review for Water Activity '{self.wateractivity.name}' by {self.user.email or self.user.phone}"


class AdventureTourCustomerReview(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    adventuretour = models.ForeignKey(
        'AdventureTour', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    review_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review for Adventure Tour '{self.adventuretour.name}' by {self.user.email or self.user.phone}"


class ComboTourCustomerReview(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    combotour = models.ForeignKey(
        'ComboTour', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    review_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review for Combo Tour '{self.combotour.name}' by {self.user.email or self.user.phone}"


class DubaiActivityCustomerReview(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    dubaiactivity = models.ForeignKey(
        'DubaiActivity', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    review_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review for Dubai Activity '{self.dubaiactivity.name}' by {self.user.email or self.user.phone}"


class Banner(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    image = models.ImageField(upload_to="banner_images/")
    theme_park = models.ForeignKey(
        ThemePark, on_delete=models.CASCADE, blank=True, null=True)
    top_attraction = models.ForeignKey(
        TopAttraction, on_delete=models.CASCADE, blank=True, null=True)
    desert_safari = models.ForeignKey(
        DesertSafari, on_delete=models.CASCADE, blank=True, null=True)
    water_park = models.ForeignKey(
        WaterPark, on_delete=models.CASCADE, blank=True, null=True)
    water_activity = models.ForeignKey(
        WaterActivity, on_delete=models.CASCADE, blank=True, null=True)
    adventure_tour = models.ForeignKey(
        AdventureTour, on_delete=models.CASCADE, blank=True, null=True)
    combo_tour = models.ForeignKey(
        ComboTour, on_delete=models.CASCADE, blank=True, null=True)
    dubai_activity = models.ForeignKey(
        DubaiActivity, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.id}"


class SelfDriveRental(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    make = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="self_drive_images/")
    registration_number = models.CharField(
        max_length=20, unique=True, null=True, blank=True)
    mileage = models.PositiveIntegerField(null=True, blank=True)
    rate_per_day = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.year} {self.make} {self.model}'


class SelfDriveRentalImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    self_drive = models.ForeignKey(SelfDriveRental, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='self_drive_images/')

    def __str__(self):
        return f"{self.self_drive.make}"
