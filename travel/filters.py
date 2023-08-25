import django_filters
from .models import Flight, Hotel, Car, Bus, Package

class FlightFilter(django_filters.FilterSet):
    departure_airport_city = django_filters.CharFilter(field_name='departure_airport__city', lookup_expr='iexact')
    arrival_airport_city = django_filters.CharFilter(field_name='arrival_airport__city', lookup_expr='iexact')
    departure_time = django_filters.DateTimeFromToRangeFilter(field_name='departure_time')
    arrival_time = django_filters.DateTimeFromToRangeFilter(field_name='arrival_time')
    price = django_filters.RangeFilter(field_name='price')

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
    available_rooms = django_filters.RangeFilter(field_name='available_rooms')
    price = django_filters.RangeFilter(field_name='price')

    def filter_amenities(self, queryset, name, value):
        amenity_ids = value.split(',')
        return queryset.filter(amenities__in=amenity_ids)

    class Meta:
        model = Hotel
        fields = []

class CarFilter(django_filters.FilterSet):
    car_type = django_filters.CharFilter(field_name='car_type__type', lookup_expr='iexact')
    fuel_type = django_filters.CharFilter(field_name='fuel_type__fuel', lookup_expr='iexact')
    seats = django_filters.RangeFilter(field_name='seats')
    transmission = django_filters.CharFilter(field_name='transmission', lookup_expr='iexact')
    ac = django_filters.BooleanFilter(field_name='ac')
    bags = django_filters.BooleanFilter(field_name='bags')
    price = django_filters.RangeFilter(field_name='price')

    class Meta:
        model = Car
        fields = []

class BusFilter(django_filters.FilterSet):
    bus_type = django_filters.CharFilter(field_name='bus_type', lookup_expr='iexact')
    departure_city = django_filters.CharFilter(field_name='departure_city', lookup_expr='iexact')
    arrival_city = django_filters.CharFilter(field_name='arrival_city', lookup_expr='iexact')
    departure_time = django_filters.DateTimeFromToRangeFilter(field_name='departure_time')
    arrival_time = django_filters.DateTimeFromToRangeFilter(field_name='arrival_time')
    available_seats = django_filters.RangeFilter(field_name='available_seats')
    price = django_filters.RangeFilter(field_name='price')

    class Meta:
        model = Bus
        fields = []

class PackageFilter(django_filters.FilterSet):
    origin_city = django_filters.CharFilter(field_name='origin_city', lookup_expr='iexact')
    destination_city = django_filters.CharFilter(field_name='destination_city', lookup_expr='iexact')
    activities = django_filters.CharFilter(field_name='activities', lookup_expr='icontains')
    price = django_filters.RangeFilter(field_name='price')

    class Meta:
        model = Package
        fields = []
