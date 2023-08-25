from rest_framework import serializers
from .models import ( Booking, Hotel, HotelAmenity, Car, AdImage,CarType,Airport,Flight,Bus,Offer,HotelImage,Airline,FuelType,Package,PackageImage)
from django.conf import settings


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = "__all__"

class FuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelType
        fields = "__all__"

class HotelAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelAmenity
        fields = ('id', 'name')

class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ('id','image')

class HotelSerializer(serializers.ModelSerializer):
    amenities = HotelAmenitySerializer(many=True)
    hotel_images = serializers.SerializerMethodField('get_hotel_images')
    class Meta:
        model = Hotel
        fields = [
            'id', 'name', 'address', 'country', 'state', 'city', 'pin', 'email', 'phone_number',
            'star_category', 'amenities', 'tax_percent', 'tax_type', 'price', 'image',
            'total_rooms', 'available_rooms','hotel_images'
        ]
    
    def get_hotel_images(self, obj):
        images = HotelImage.objects.filter(hotel=obj.id)
        serializer = HotelImageSerializer(images, many=True)
        return [{'id':image['id'],'image':self._get_image_url(image['image'])} for image in serializer.data]

    def _get_image_url(self, image_path):
        return self.context['request'].build_absolute_uri(settings.MEDIA_URL + image_path.replace('/media/',''))
    

class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    car_type = CarTypeSerializer(many=False,read_only=True)
    fuel_type = FuelTypeSerializer(many=False,read_only=True)
    class Meta:
        model = Car
        fields = '__all__'

class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['id','image']

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'

class FlightSerializer(serializers.ModelSerializer):
    departure_airport = AirportSerializer(many=False,read_only=True)
    arrival_airport = AirportSerializer(many=False,read_only=True)
    airline = AirlineSerializer(many=False,read_only=True)
    class Meta:
        model = Flight
        fields = "__all__"


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = "__all__"

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"

class PackageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageImage
        fields = "__all__"

class PackageSerializer(serializers.ModelSerializer):
    flights = FlightSerializer(many=True)
    cars = CarSerializer(many=True)
    buses = BusSerializer(many=True)
    hotels = HotelSerializer(many=True)
    images = serializers.SerializerMethodField('get_hotel_images')
    
    class Meta:
        model = Package
        fields = ['id', 'name', 'origin_city', 'destination_city', 'price', 'flights', 'cars', 'buses', 'hotels', 'activities', 'duration','images']
    
    def get_hotel_images(self, obj):
        images = PackageImage.objects.filter(package=obj.id)
        serializer = PackageImageSerializer(images, many=True)
        return [{'id':image['id'],'image':self._get_image_url(image['image'])} for image in serializer.data]

    def _get_image_url(self, image_path):
        return self.context['request'].build_absolute_uri(settings.MEDIA_URL + image_path.replace('/media/',''))