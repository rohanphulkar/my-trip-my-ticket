from rest_framework import serializers
from .models import *
from django.conf import settings
from accounts.serializers import *
from django.db.models import Sum

# Customer Review Serializer


class HotelCustomerReviewSerializer(serializers.ModelSerializer):
    users_data = serializers.SerializerMethodField('get_user_data')

    class Meta:
        model = HotelCustomerReview
        fields = '__all__'

    def get_user_data(self, obj):
        user_data = UserSerializer(obj.user).data
        return {
            'email': user_data.get('email'),
            'phone': user_data.get('phone')
        }


class CarCustomerReviewSerializer(serializers.ModelSerializer):
    users_data = serializers.SerializerMethodField('get_user_data')

    class Meta:
        model = CarCustomerReview
        fields = '__all__'

    def get_user_data(self, obj):
        user_data = UserSerializer(obj.user).data
        return {
            'email': user_data.get('email'),
            'phone': user_data.get('phone')
        }


class FlightCustomerReviewSerializer(serializers.ModelSerializer):
    users_data = serializers.SerializerMethodField('get_user_data')

    class Meta:
        model = FlightCustomerReview
        fields = '__all__'

    def get_user_data(self, obj):
        user_data = UserSerializer(obj.user).data
        return {
            'email': user_data.get('email'),
            'phone': user_data.get('phone')
        }


class PackageCustomerReviewSerializer(serializers.ModelSerializer):
    users_data = serializers.SerializerMethodField('get_user_data')

    class Meta:
        model = PackageCustomerReview
        fields = '__all__'

    def get_user_data(self, obj):
        user_data = UserSerializer(obj.user).data
        return {
            'email': user_data.get('email'),
            'phone': user_data.get('phone')
        }


class ThemeParkCustomerReviewSerializer(serializers.ModelSerializer):
    users_data = serializers.SerializerMethodField('get_user_data')

    class Meta:
        model = ThemeParkCustomerReview
        fields = '__all__'

    def get_user_data(self, obj):
        user_data = UserSerializer(obj.user).data
        return {
            'email': user_data.get('email'),
            'phone': user_data.get('phone')
        }


class TopAttractionCustomerReviewSerializer(serializers.ModelSerializer):
    users_data = serializers.SerializerMethodField('get_user_data')

    class Meta:
        model = TopAttractionCustomerReview
        fields = '__all__'

    def get_user_data(self, obj):
        user_data = UserSerializer(obj.user).data
        return {
            'email': user_data.get('email'),
            'phone': user_data.get('phone')
        }


class DesertSafariCustomerReviewSerializer(serializers.ModelSerializer):
    users_data = serializers.SerializerMethodField('get_user_data')

    class Meta:
        model = DesertSafariCustomerReview
        fields = '__all__'

    def get_user_data(self, obj):
        user_data = UserSerializer(obj.user).data
        return {
            'email': user_data.get('email'),
            'phone': user_data.get('phone')
        }


class WaterParkCustomerReviewSerializer(serializers.ModelSerializer):
    users_data = serializers.SerializerMethodField('get_user_data')

    class Meta:
        model = WaterParkCustomerReview
        fields = '__all__'

    def get_user_data(self, obj):
        user_data = UserSerializer(obj.user).data
        return {
            'email': user_data.get('email'),
            'phone': user_data.get('phone')
        }


class WaterActivityCustomerReviewSerializer(serializers.ModelSerializer):
    users_data = serializers.SerializerMethodField('get_user_data')

    class Meta:
        model = WaterActivityCustomerReview
        fields = '__all__'

    def get_user_data(self, obj):
        user_data = UserSerializer(obj.user).data
        return {
            'email': user_data.get('email'),
            'phone': user_data.get('phone')
        }


class AdventureTourCustomerReviewSerializer(serializers.ModelSerializer):
    users_data = serializers.SerializerMethodField('get_user_data')

    class Meta:
        model = AdventureTourCustomerReview
        fields = '__all__'

    def get_user_data(self, obj):
        user_data = UserSerializer(obj.user).data
        return {
            'email': user_data.get('email'),
            'phone': user_data.get('phone')
        }


class ComboTourCustomerReviewSerializer(serializers.ModelSerializer):
    users_data = serializers.SerializerMethodField('get_user_data')

    class Meta:
        model = ComboTourCustomerReview
        fields = '__all__'

    def get_user_data(self, obj):
        user_data = UserSerializer(obj.user).data
        return {
            'email': user_data.get('email'),
            'phone': user_data.get('phone')
        }


class DubaiActivityCustomerReviewSerializer(serializers.ModelSerializer):
    users_data = serializers.SerializerMethodField('get_user_data')

    class Meta:
        model = DubaiActivityCustomerReview
        fields = '__all__'

    def get_user_data(self, obj):
        user_data = UserSerializer(obj.user).data
        return {
            'email': user_data.get('email'),
            'phone': user_data.get('phone')
        }


class YachtCustomerReviewSerializer(serializers.ModelSerializer):
    users_data = serializers.SerializerMethodField('get_user_data')

    class Meta:
        model = YachtCustomerReview
        fields = '__all__'

    def get_user_data(self, obj):
        user_data = UserSerializer(obj.user).data
        return {
            'email': user_data.get('email'),
            'phone': user_data.get('phone')
        }


# Hotel Serializers
class HotelAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelAmenity
        fields = ['id', 'name', 'description', 'additional_cost']


class RoomSerializer(serializers.ModelSerializer):
    amenities = serializers.SerializerMethodField('get_amenities')

    class Meta:
        model = Room
        fields = ['id', 'hotel', 'room_type', 'capacity', 'price', 'availability',
                  'image', 'bed_type', 'view', 'smoking_allowed', 'pet_friendly', 'amenities']

    def get_amenities(self, obj):
        amenities = HotelAmenity.objects.filter(rooms=obj.id)
        serializer = HotelAmenitySerializer(amenities, many=True)
        return serializer.data


class YachtImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = YachtImage
        fields = "__all__"


class YachtSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_yacht_images')
    reviews = YachtCustomerReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Yacht
        fields = "__all__"

    def get_yacht_images(self, obj):
        images = YachtImage.objects.filter(yacht=obj.id)
        serializer = YachtImageSerializer(images, many=True)
        return [{'id': image['id'], 'image':image['image']} for image in serializer.data]


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ('id', 'image')


class HotelSerializer(serializers.ModelSerializer):
    amenities = HotelAmenitySerializer(many=True)
    hotel_images = serializers.SerializerMethodField('get_hotel_images')
    available_rooms = serializers.SerializerMethodField('get_available_rooms')
    rooms = RoomSerializer(many=True, read_only=True)
    reviews = HotelCustomerReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'description', 'address', 'country', 'state', 'city', 'pin', 'email', 'phone_number', 'star_category', 'amenities', 'tax_percent', 'tax_type',
                  'price', 'image', 'total_rooms', 'available_rooms', 'available_from', 'available_to', 'website', 'wifi_available', 'parking_available', 'rooms', 'hotel_images', 'reviews']

    def get_hotel_images(self, obj):
        images = HotelImage.objects.filter(hotel=obj.id)
        serializer = HotelImageSerializer(images, many=True)
        return [{'id': image['id'], 'image':image['image']} for image in serializer.data]

    def get_available_rooms(self, obj):
        total_available_rooms = Room.objects.filter(hotel=obj.id).aggregate(
            total_available_rooms=Sum('available_rooms'))['total_available_rooms']
        return total_available_rooms


# Car Serializers
class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = '__all__'


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ('id', 'image')


class CarSerializer(serializers.ModelSerializer):
    car_type = CarTypeSerializer(many=False, read_only=True)
    car_images = serializers.SerializerMethodField('get_car_images')
    reviews = CarCustomerReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'name', 'address', 'country', 'state', 'city', 'pin', 'email', 'phone_number', 'origin_city', 'destination_city', 'make', 'model', 'car_type', 'seats',
                  'transmission_type', 'fuel_type', 'ac', 'bags', 'image', 'price', 'tax_percent', 'tax_type', 'total_cars', 'available_cars', 'available_till', 'car_images', 'reviews']

    def get_car_images(self, obj):
        images = CarImage.objects.filter(car=obj.id)
        serializer = CarImageSerializer(images, many=True)
        return [{'id': image['id'], 'image':image['image']} for image in serializer.data]


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
    departure_airport = AirportSerializer(many=False, read_only=True)
    arrival_airport = AirportSerializer(many=False, read_only=True)
    airline = AirlineSerializer(many=False, read_only=True)
    amenities = FlightAmenitySerializer(many=True, read_only=True)
    reviews = FlightCustomerReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = "__all__"


# Bus Serializers
class BusAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusAmenity
        fields = '__all__'


class BusSerializer(serializers.ModelSerializer):
    amenities = BusAmenitySerializer(many=True, read_only=True)

    class Meta:
        model = Bus
        fields = ['id', 'bus_number', 'bus_type', 'operator', 'departure_station', 'arrival_station', 'departure_date', 'departure_time', 'arrival_date',
                  'arrival_time', 'duration', 'price', 'total_seats', 'available_seats', 'amenities', 'wifi_available', 'power_outlets_available', 'refreshments_served']


class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = "__all__"


class PackageSerializer(serializers.ModelSerializer):
    flights = FlightSerializer(many=True)
    cars = CarSerializer(many=True)
    buses = BusSerializer(many=True)
    hotels = HotelSerializer(many=True)
    reviews = PackageCustomerReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = ['id', 'name', 'image', 'origin_city', 'destination_city', 'category', 'price', 'flights', 'cars', 'buses',
                  'hotels', 'activities', 'duration', 'included_meals', 'departure', 'with_flights', 'total_rooms', 'reviews']


class ReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'


class HotelReservationSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer(many=False, read_only=True)
    room = RoomSerializer(many=False, read_only=True)

    class Meta:
        model = HotelReservation
        fields = '__all__'


class YachtReservationSerializer(serializers.ModelSerializer):
    yacht = YachtSerializer(many=False, read_only=True)

    class Meta:
        model = YachtReservation
        fields = '__all__'


class CarReservationSerializer(serializers.ModelSerializer):
    car = CarSerializer(many=False, read_only=True)

    class Meta:
        model = CarReservation
        fields = '__all__'


class FlightReservationSerializer(serializers.ModelSerializer):
    flight = FlightSerializer(many=False, read_only=True)

    class Meta:
        model = FlightReservation
        fields = '__all__'


class BusReservationSerializer(serializers.ModelSerializer):
    bus = BusSerializer(many=False, read_only=True)

    class Meta:
        model = BusReservation
        fields = '__all__'


class PackageReservationSerializer(serializers.ModelSerializer):
    package = PackageSerializer(many=False, read_only=True)

    class Meta:
        model = PackageReservation
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)
    hotel = HotelReservationSerializer(read_only=True, many=False)
    car = CarReservationSerializer(read_only=True, many=False)
    flight = FlightReservationSerializer(read_only=True, many=False)
    bus = BusReservationSerializer(read_only=True, many=False)
    package = PackageReservationSerializer(read_only=True, many=False)
    yacht = YachtReservationSerializer(read_only=True, many=False)

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
        fields = ['name', 'email', 'location', 'currency', 'quantity',
                  'purpose_of_visit', 'booking_currency_for', 'amount', 'action']


class VisaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visa
        fields = ['name', 'email', 'country', 'visa_type', 'traveller']


class ThemeParkImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeParkImage
        fields = '__all__'


class ThemeParkSerializer(serializers.ModelSerializer):
    reviews = ThemeParkCustomerReviewSerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField('get_images')

    class Meta:
        model = ThemePark
        fields = '__all__'

    def get_images(self, obj):
        images = ThemeParkImage.objects.filter(theme_park=obj.id)
        serializer = ThemeParkImageSerializer(images, many=True)
        return serializer.data


class TopAttractionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopAttractionImage
        fields = '__all__'


class TopAttractionSerializer(serializers.ModelSerializer):
    reviews = TopAttractionCustomerReviewSerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField('get_images')

    class Meta:
        model = TopAttraction
        fields = '__all__'

    def get_images(self, obj):
        images = TopAttractionImage.objects.filter(top_attraction=obj.id)
        serializer = TopAttractionImageSerializer(images, many=True)
        return serializer.data


class DesertSafariImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesertSafariImage
        fields = '__all__'


class DesertSafariSerializer(serializers.ModelSerializer):
    reviews = DesertSafariCustomerReviewSerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField('get_images')

    class Meta:
        model = DesertSafari
        fields = '__all__'

    def get_images(self, obj):
        images = DesertSafariImage.objects.filter(desert_safari=obj.id)
        serializer = DesertSafariImageSerializer(images, many=True)
        return serializer.data


class WaterParkImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterParkImage
        fields = '__all__'


class WaterParkSerializer(serializers.ModelSerializer):
    reviews = WaterParkCustomerReviewSerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField('get_images')

    class Meta:
        model = WaterPark
        fields = '__all__'

    def get_images(self, obj):
        images = WaterParkImage.objects.filter(water_park=obj.id)
        serializer = WaterParkImageSerializer(images, many=True)
        return serializer.data


class WaterActivityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterActivityImage
        fields = '__all__'


class WaterActivitySerializer(serializers.ModelSerializer):
    reviews = WaterActivityCustomerReviewSerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField('get_images')

    class Meta:
        model = WaterActivity
        fields = '__all__'

    def get_images(self, obj):
        images = WaterActivityImage.objects.filter(water_activity=obj.id)
        serializer = WaterActivityImageSerializer(images, many=True)
        return serializer.data


class AdventureTourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdventureTourImage
        fields = '__all__'


class AdventureTourSerializer(serializers.ModelSerializer):
    reviews = AdventureTourCustomerReviewSerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField('get_images')

    class Meta:
        model = AdventureTour
        fields = '__all__'

    def get_images(self, obj):
        images = AdventureTourImage.objects.filter(adventure_tour=obj.id)
        serializer = AdventureTourImageSerializer(images, many=True)
        return serializer.data


class ComboTourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComboTourImage
        fields = '__all__'


class ComboTourSerializer(serializers.ModelSerializer):
    reviews = ComboTourCustomerReviewSerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField('get_images')

    class Meta:
        model = ComboTour
        fields = '__all__'

    def get_images(self, obj):
        images = ComboTourImage.objects.filter(combo_tour=obj.id)
        serializer = ComboTourImageSerializer(images, many=True)
        return serializer.data


class DubaiActivityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DubaiActivityImage
        fields = '__all__'


class DubaiActivitySerializer(serializers.ModelSerializer):
    reviews = DubaiActivityCustomerReviewSerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField('get_images')

    class Meta:
        model = DubaiActivity
        fields = '__all__'

    def get_images(self, obj):
        images = DubaiActivityImage.objects.filter(dubai_activity=obj.id)
        serializer = DubaiActivityImageSerializer(images, many=True)
        return serializer.data
    
class CityTourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityTourImage
        fields = ('image',)

class CityTourSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_images')

    class Meta:
        model = CityTour
        fields = '__all__'
    
    def get_images(self, obj):
        images = CityTourImage.objects.filter(city_tour=obj.id)
        serializer = CityTourImageSerializer(images, many=True)
        return serializer.data


class ThemeParkReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeParkReservation
        fields = '__all__'


class TopAttractionReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopAttractionReservation
        fields = '__all__'


class DesertSafariReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesertSafariReservation
        fields = '__all__'


class WaterParkReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterParkReservation
        fields = '__all__'


class WaterActivityReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterActivityReservation
        fields = '__all__'


class AdventureTourReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdventureTourReservation
        fields = '__all__'


class ComboTourReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComboTourReservation
        fields = '__all__'


class DubaiActivityReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DubaiActivityReservation
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    theme_park = ThemeParkSerializer(many=False, read_only=True)
    top_attraction = TopAttractionSerializer(many=False, read_only=True)
    desert_safari = DesertSafariSerializer(many=False, read_only=True)
    water_park = WaterParkSerializer(many=False, read_only=True)
    water_activity = WaterActivitySerializer(many=False, read_only=True)
    adventure_tour = AdventureTourSerializer(many=False, read_only=True)
    combo_tour = ComboTourSerializer(many=False, read_only=True)
    dubai_activity = DubaiActivitySerializer(many=False, read_only=True)

    class Meta:
        model = Banner
        fields = "__all__"

class SelfDriveRentalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfDriveRentalImage
        fields = "__all__"

class SelfDriveRentalSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_images')
    class Meta:
        model = SelfDriveRental
        fields = '__all__'
    
    def get_images(self, obj):
        images = SelfDriveRentalImage.objects.filter(self_drive=obj.id)
        serializer = SelfDriveRentalImageSerializer(images, many=True)
        return serializer.data
