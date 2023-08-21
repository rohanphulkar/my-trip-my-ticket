from rest_framework import serializers
from .models import Tour, Booking, Hotel, HotelAmenity, Car, AdImage, UserItinerary,CarType

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class HotelAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelAmenity
        fields = '__all__'

class HotelSerializer(serializers.ModelSerializer):
    amenities = HotelAmenitySerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = '__all__'

class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    car_type = CarTypeSerializer(many=False,read_only=True)
    class Meta:
        model = Car
        fields = '__all__'

class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['id','image']
