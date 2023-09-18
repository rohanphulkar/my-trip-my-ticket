from django.contrib import admin
from .models import *

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_booking_type', 'status', 'check_in_date', 'check_out_date')

    def get_booking_type(self, obj):
        if obj.hotel:
            return 'Hotel'
        elif obj.car:
            return 'Car'
        elif obj.flight:
            return 'Flight'
        elif obj.bus:
            return 'Bus'
        return 'Unknown'
    
    get_booking_type.short_description = 'Booking Type'

# Define an inline class for HotelImage
class HotelImageAdmin(admin.StackedInline):
    model = HotelImage

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['hotel','room_type','price']

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'star_category')
    filter_horizontal = ('amenities',)
    inlines = [HotelImageAdmin]

@admin.register(HotelAmenity)
class HotelAmenityAdmin(admin.ModelAdmin):
    pass

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'car_type')

@admin.register(AdImage)
class AdImageAdmin(admin.ModelAdmin):
    pass

@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ['type']

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'city', 'country')
    list_filter = ('country', 'city')
    search_fields = ('code', 'name', 'city', 'country')

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'price', 'available_seats')
    list_filter = ('departure_airport__city', 'arrival_airport__city')
    search_fields = ('departure_airport__code', 'arrival_airport__code')

@admin.register(FlightAmenity)
class FlightAmenityAdmin(admin.ModelAdmin):
    pass

admin.site.register(BusAmenity)

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_number', 'operator', 'departure_station', 'arrival_station', 'departure_time', 'arrival_time', 'available_seats')
    list_filter = ('operator', 'departure_station', 'arrival_station')
    search_fields = ('bus_number', 'operator', 'departure_station', 'arrival_station')

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'discount_percent', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('code', 'description')

@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')
    

@admin.register(Forex)
class ForexAdmin(admin.ModelAdmin):
    list_display = ('location', 'currency', 'quantity', 'purpose_of_visit', 'booking_currency_for', 'amount')


@admin.register(HotelReservation)
class HotelReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'hotel', 'room', 'status', 'reservation_date']
    list_filter = ['status', 'reservation_date']
    search_fields = ['user__email', 'hotel__name', 'room__name']

@admin.register(CarReservation)
class CarReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'rental_start_date', 'rental_end_date', 'status', 'reservation_date']
    list_filter = ['status', 'reservation_date']
    search_fields = ['user__email', 'car__make','car__model']

@admin.register(FlightReservation)
class FlightReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'flight', 'departure_on', 'status', 'reservation_date']
    list_filter = ['status', 'reservation_date']
    search_fields = ['user__email', 'flight__name']

@admin.register(BusReservation)
class BusReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'bus', 'departure_on', 'status', 'reservation_date']
    list_filter = ['status', 'reservation_date']
    search_fields = ['user__email', 'bus__number']

@admin.register(PackageReservation)
class PackageReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'package', 'status', 'reservation_date']
    list_filter = ['status', 'reservation_date']
    search_fields = ['user__email', 'package__name']
    

@admin.register(DubaiActivity)
class DubaiActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    list_filter = ('price',)