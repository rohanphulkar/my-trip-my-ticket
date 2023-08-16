from django.contrib import admin
from .models import Tour, Booking, Hotel, HotelAmenity, Car, AdImage, UserItinerary,CarType

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'status', 'check_in_date', 'check_out_date')

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'star_category')
    filter_horizontal = ('amenities',)

@admin.register(HotelAmenity)
class HotelAmenityAdmin(admin.ModelAdmin):
    pass

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'car_type')


@admin.register(AdImage)
class AdImageAdmin(admin.ModelAdmin):
    pass

@admin.register(UserItinerary)
class UserItineraryAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'date', 'time')

@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ['type']