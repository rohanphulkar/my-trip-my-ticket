from django.contrib import admin
from .models import (
    Tour, Booking, Hotel, HotelAmenity, Car, AdImage, CarType,
    TourImage, HotelImage, CarImage,Airport,Flight,Bus,Offer
)

class TourImageAdmin(admin.StackedInline):
    model = TourImage


class HotelImageAdmin(admin.StackedInline):
    model = HotelImage


class CarImageAdmin(admin.StackedInline):
    model = CarImage

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price')
    inlines = [TourImageAdmin]

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'check_in_date', 'check_out_date')
    

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
    inlines = [CarImageAdmin]

@admin.register(AdImage)
class AdImageAdmin(admin.ModelAdmin):
    pass

@admin.register(UserItinerary)
class UserItineraryAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'date', 'time')

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

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_number', 'operator', 'departure_city', 'arrival_city', 'departure_datetime', 'arrival_datetime', 'available_seats')
    list_filter = ('operator', 'departure_city', 'arrival_city')
    search_fields = ('bus_number', 'operator', 'departure_city', 'arrival_city')

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'discount_percent', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('code', 'description')