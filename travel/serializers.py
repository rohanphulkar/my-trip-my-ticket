from rest_framework import serializers
from .models import *
from django.conf import settings
from accounts.serializers import *
from django.db.models import Sum

# Hotel Serializers
class HotelAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelAmenity
        fields = ['id', 'name', 'description', 'additional_cost']

class RoomSerializer(serializers.ModelSerializer):
    amenities = serializers.SerializerMethodField('get_amenities')
    class Meta:
        model = Room
        fields =['id', 'hotel', 'room_type', 'capacity', 'price', 'availability', 'image', 'bed_type', 'view', 'smoking_allowed', 'pet_friendly','amenities']
        
    def get_amenities(self,obj):
        amenities = HotelAmenity.objects.filter(rooms=obj.id)
        serializer = HotelAmenitySerializer(amenities,many=True)
        return serializer.data
    
        



class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ('id','image')

class HotelSerializer(serializers.ModelSerializer):
    amenities = HotelAmenitySerializer(many=True)
    hotel_images = serializers.SerializerMethodField('get_hotel_images')
    available_rooms = serializers.SerializerMethodField('get_available_rooms')
    rooms = RoomSerializer(many=True,read_only=True)
    class Meta:
        model = Hotel
        fields = ['id', 'name','description', 'address', 'country', 'state', 'city', 'pin', 'email', 'phone_number', 'star_category', 'amenities', 'tax_percent', 'tax_type', 'price', 'image', 'total_rooms', 'available_rooms', 'available_from', 'available_to', 'website', 'wifi_available', 'parking_available','rooms','hotel_images']
    
    def get_hotel_images(self, obj):
        images = HotelImage.objects.filter(hotel=obj.id)
        serializer = HotelImageSerializer(images, many=True)
        return [{'id':image['id'],'image':self._get_image_url(image['image'])} for image in serializer.data]

    def _get_image_url(self, image_path):
        return self.context['request'].build_absolute_uri(settings.MEDIA_URL + image_path.replace('/media/',''))
    
    def get_available_rooms(self,obj):
        total_available_rooms = Room.objects.filter(hotel=obj.id).aggregate(total_available_rooms=Sum('available_rooms'))['total_available_rooms']
        return total_available_rooms
    
    

# Car Serializers
class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = '__all__'
        
class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ('id','image')

class CarSerializer(serializers.ModelSerializer):
    car_type = CarTypeSerializer(many=False,read_only=True)
    car_images = serializers.SerializerMethodField('get_car_images')
    
    class Meta:
        model = Car
        fields = ['id', 'name', 'address', 'country', 'state', 'city', 'pin', 'email', 'phone_number', 'origin_city', 'destination_city', 'make', 'model', 'car_type', 'seats', 'transmission_type', 'fuel_type', 'ac', 'bags', 'image', 'price', 'tax_percent', 'tax_type', 'total_cars', 'available_cars', 'available_till','car_images']
    
    def get_car_images(self, obj):
        images = CarImage.objects.filter(car=obj.id)
        serializer = CarImageSerializer(images, many=True)
        return [{'id':image['id'],'image':self._get_image_url(image['image'])} for image in serializer.data]

    def _get_image_url(self, image_path):
        return self.context['request'].build_absolute_uri(settings.MEDIA_URL + image_path.replace('/media/',''))

class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['id','image']


# Flight Serializers

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = "__all__"

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'

class FlightAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightAmenity
        fields = '__all__'

class FlightSerializer(serializers.ModelSerializer):
    departure_airport = AirportSerializer(many=False,read_only=True)
    arrival_airport = AirportSerializer(many=False,read_only=True)
    airline = AirlineSerializer(many=False,read_only=True)
    amenities = FlightAmenitySerializer(many=True,read_only=True)
    class Meta:
        model = Flight
        fields = "__all__"


# Bus Serializers
class BusAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusAmenity
        fields = '__all__'

class BusSerializer(serializers.ModelSerializer):
    amenities = BusAmenitySerializer(many=True,read_only=True)
    class Meta:
        model = Bus
        fields = ['id', 'bus_number', 'bus_type', 'operator', 'departure_station', 'arrival_station', 'departure_date', 'departure_time', 'arrival_date', 'arrival_time', 'duration', 'price', 'total_seats', 'available_seats', 'amenities', 'wifi_available', 'power_outlets_available', 'refreshments_served']

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"



class PackageSerializer(serializers.ModelSerializer):
    flights = FlightSerializer(many=True)
    cars = CarSerializer(many=True)
    buses = BusSerializer(many=True)
    hotels = HotelSerializer(many=True)
    
    class Meta:
        model = Package
        fields = ['id', 'name', 'image', 'origin_city', 'destination_city', 'price', 'flights', 'cars', 'buses', 'hotels', 'activities', 'duration', 'included_meals', 'departure', 'with_flights', 'total_rooms']


class ReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False,read_only=True)
    class Meta:
        model = Reservation
        fields = '__all__'

class HotelReservationSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer(many=False,read_only=True)
    room = RoomSerializer(many=False,read_only=True)
    class Meta:
        model = HotelReservation
        fields = '__all__'

class CarReservationSerializer(serializers.ModelSerializer):
    car = CarSerializer(many=False,read_only=True)
    class Meta:
        model = CarReservation
        fields = '__all__'

class FlightReservationSerializer(serializers.ModelSerializer):
    flight = FlightSerializer(many=False,read_only=True)
    class Meta:
        model = FlightReservation
        fields = '__all__'

class BusReservationSerializer(serializers.ModelSerializer):
    bus = BusSerializer(many=False,read_only=True)

    class Meta:
        model = BusReservation
        fields = '__all__'

class PackageReservationSerializer(serializers.ModelSerializer):
    package = PackageSerializer(many=False,read_only=True)
    class Meta:
        model = PackageReservation
        fields = '__all__'
    

class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True,many=False)
    hotel = HotelReservationSerializer(read_only=True,many=False)
    car = CarReservationSerializer(read_only=True,many=False)
    flight = FlightReservationSerializer(read_only=True,many=False)
    bus = BusReservationSerializer(read_only=True,many=False)
    package = PackageReservationSerializer(read_only=True,many=False)
    class Meta:
        model = Booking
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        
        
class ForexCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forex
        fields = ['name','email','location', 'currency', 'quantity', 'purpose_of_visit', 'booking_currency_for', 'amount','action']
        
class DubaiActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DubaiActivity
        fields = ('id', 'name', 'description', 'image', 'price')