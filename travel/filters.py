import django_filters
from django.db.models import Q
from .models import Flight, Hotel, Car, Bus, Package, Booking

class FlightFilter(django_filters.FilterSet):
    departure_airport_city = django_filters.CharFilter(field_name='departure_airport__city', lookup_expr='iexact')
    arrival_airport_city = django_filters.CharFilter(field_name='arrival_airport__city', lookup_expr='iexact')
    departure_time = django_filters.DateFromToRangeFilter(field_name='departure_time')
    arrival_time = django_filters.DateFromToRangeFilter(field_name='arrival_time')
    available_seats = django_filters.RangeFilter(field_name='available_seats', lookup_expr='iexact')
    cabin_class = django_filters.CharFilter(field_name='cabin_class', lookup_expr='iexact')
    price = django_filters.RangeFilter(field_name='price')
    wifi_available = django_filters.BooleanFilter(field_name='wifi_available')
    in_flight_meal = django_filters.BooleanFilter(field_name='in_flight_meal')

    class Meta:
        model = Flight
        fields = []

class HotelFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name='city', lookup_expr='iexact')
    pin = django_filters.CharFilter(field_name='pin', lookup_expr='iexact')
    star_category = django_filters.ChoiceFilter(field_name='star_category', choices=Hotel.STAR_CATEGORY_CHOICES)
    amenities = django_filters.CharFilter(method='filter_amenities')
    tax_type = django_filters.CharFilter(field_name='tax_type', lookup_expr='iexact')
    tax_percent = django_filters.RangeFilter(field_name='tax_percent')
    total_rooms = django_filters.RangeFilter(field_name='total_rooms')
    available_rooms = django_filters.RangeFilter(field_name='rooms__available_rooms')
    price = django_filters.RangeFilter(field_name='rooms__price')
    available_from = django_filters.DateFromToRangeFilter(field_name='available_from',lookup_expr='gte')
    available_to = django_filters.DateFromToRangeFilter(field_name='available_to',lookup_expr='lte')
    wifi_available = django_filters.BooleanFilter(field_name='wifi_available')
    parking_available = django_filters.BooleanFilter(field_name='parking_available')

    def filter_amenities(self, queryset, name, value):
        amenity_ids = value.split(',')
        return queryset.filter(amenities__in=amenity_ids)

    class Meta:
        model = Hotel
        fields = []

class CarFilter(django_filters.FilterSet):
    car_type = django_filters.CharFilter(field_name='car_type__type', lookup_expr='iexact')
    seats = django_filters.RangeFilter(field_name='seats')
    ac = django_filters.BooleanFilter(field_name='ac')
    bags = django_filters.BooleanFilter(field_name='bags')
    price = django_filters.RangeFilter(field_name='price')
    origin_city = django_filters.CharFilter(field_name='origin_city', lookup_expr='iexact')
    destination_city = django_filters.CharFilter(field_name='destination_city', lookup_expr='iexact')
    available_till = django_filters.DateFromToRangeFilter(field_name='available_till',lookup_expr='lte')

    class Meta:
        model = Car
        fields = []

class BusFilter(django_filters.FilterSet):
    departure_station = django_filters.CharFilter(field_name='departure_station', lookup_expr='iexact')
    arrival_station = django_filters.CharFilter(field_name='arrival_station', lookup_expr='iexact')
    departure_date = django_filters.DateFromToRangeFilter(field_name='departure_date')
    departure_time = django_filters.TimeRangeFilter(field_name='departure_time')
    arrival_date = django_filters.DateFromToRangeFilter(field_name='arrival_date')
    arrival_time = django_filters.TimeRangeFilter(field_name='arrival_time')
    bus_type = django_filters.CharFilter(field_name='bus_type', lookup_expr='iexact')
    wifi_available = django_filters.BooleanFilter(field_name='wifi_available')
    power_outlets_available = django_filters.BooleanFilter(field_name='power_outlets_available')
    refreshments_served = django_filters.BooleanFilter(field_name='refreshments_served')

    class Meta:
        model = Bus
        fields = []

class PackageFilter(django_filters.FilterSet):
    origin_city = django_filters.CharFilter(field_name='origin_city', lookup_expr='icontains')
    destination_city = django_filters.CharFilter(field_name='destination_city', lookup_expr='icontains')
    activities = django_filters.CharFilter(field_name='activities', lookup_expr='icontains')
    departure = django_filters.DateFromToRangeFilter(field_name='departure')
    star_category = django_filters.CharFilter(field_name='hotels__star_category', lookup_expr='iexact')
    price = django_filters.RangeFilter(field_name='price')
    with_flights = django_filters.BooleanFilter(field_name='with_flights')
    total_rooms = django_filters.RangeFilter(field_name='total_rooms')

    class Meta:
        model = Package
        fields = []

class BookingFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')

    class Meta:
        model = Booking
        fields = []
