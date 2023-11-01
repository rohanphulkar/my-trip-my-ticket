from django.contrib import admin
from .models import *


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_booking_type', 'status', 'booking_date')

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
    list_display = ['hotel', 'room_type', 'price']


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'star_category')
    filter_horizontal = ('amenities',)
    inlines = [HotelImageAdmin]


@admin.register(HotelAmenity)
class HotelAmenityAdmin(admin.ModelAdmin):
    pass


class CarImageAdmin(admin.StackedInline):
    model = CarImage


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'car_type')
    inlines = [CarImageAdmin]


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
    list_display = ('departure_airport', 'arrival_airport',
                    'departure_time', 'arrival_time', 'price', 'available_seats')
    list_filter = ('departure_airport__city', 'arrival_airport__city')
    search_fields = ('departure_airport__code', 'arrival_airport__code')


@admin.register(FlightAmenity)
class FlightAmenityAdmin(admin.ModelAdmin):
    pass


admin.site.register(BusAmenity)


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_number', 'operator', 'departure_station',
                    'arrival_station', 'departure_time', 'arrival_time', 'available_seats')
    list_filter = ('operator', 'departure_station', 'arrival_station')
    search_fields = ('bus_number', 'operator',
                     'departure_station', 'arrival_station')


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('code', 'image', 'discount_percent',
                    'start_date', 'end_date')
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
    list_display = ('location', 'currency', 'quantity',
                    'purpose_of_visit', 'booking_currency_for', 'amount')


@admin.register(Visa)
class VisaAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'country', 'visa_type', 'traveller')


@admin.register(HotelReservation)
class HotelReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'hotel', 'room', 'status', 'reservation_date']
    list_filter = ['status', 'reservation_date']
    search_fields = ['user__email', 'hotel__name', 'room__name']


@admin.register(CarReservation)
class CarReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'rental_start_date',
                    'rental_end_date', 'status', 'reservation_date']
    list_filter = ['status', 'reservation_date']
    search_fields = ['user__email', 'car__make', 'car__model']


@admin.register(FlightReservation)
class FlightReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'flight',
                    'departure_on', 'status', 'reservation_date']
    list_filter = ['status', 'reservation_date']
    search_fields = ['user__email', 'flight__name']


@admin.register(BusReservation)
class BusReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'bus', 'departure_on',
                    'status', 'reservation_date']
    list_filter = ['status', 'reservation_date']
    search_fields = ['user__email', 'bus__number']


@admin.register(PackageReservation)
class PackageReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'package', 'status', 'reservation_date']
    list_filter = ['status', 'reservation_date']
    search_fields = ['user__email', 'package__name']


class YachtImageAdmin(admin.StackedInline):
    model = YachtImage


@admin.register(Yacht)
class YachtAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'size', 'capacity', 'charter_price'
    )
    search_fields = ('name', 'manufacturer', 'registration_country')
    inlines = [YachtImageAdmin]


@admin.register(YachtReservation)
class YachtReservationAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'yacht', 'check_in_date', 'check_out_date', 'status', 'reservation_date'
    )
    list_filter = ('status', 'reservation_date')
    search_fields = ('user__email', 'yacht__name')


class ThemeParkImageAdmin(admin.StackedInline):
    model = ThemeParkImage


@admin.register(ThemePark)
class ThemeParkAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'opening_date', 'price')
    search_fields = ('name', 'location')
    inlines = [ThemeParkImageAdmin]


class TopAttractionImageAdmin(admin.StackedInline):
    model = TopAttractionImage


@admin.register(TopAttraction)
class TopAttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'theme_park', 'thrill_level', 'price')
    list_filter = ('theme_park', 'thrill_level')
    search_fields = ('name', 'theme_park__name')
    inlines = [TopAttractionImageAdmin]


class DesertSafariImageAdmin(admin.StackedInline):
    model = DesertSafariImage


@admin.register(DesertSafari)
class DesertSafariAdmin(admin.ModelAdmin):
    list_display = ('location', 'duration_hours', 'price')
    search_fields = ('location',)
    inlines = [DesertSafariImageAdmin]


class WaterParkImageAdmin(admin.StackedInline):
    model = WaterParkImage


@admin.register(WaterPark)
class WaterParkAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'opening_date', 'price')
    search_fields = ('name', 'location')
    inlines = [WaterParkImageAdmin]


class WaterActivityImageAdmin(admin.StackedInline):
    model = WaterActivityImage


@admin.register(WaterActivity)
class WaterActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'water_park', 'age_limit', 'price')
    list_filter = ('water_park',)
    search_fields = ('name', 'water_park__name')
    inlines = [WaterActivityImageAdmin]


class AdventureTourImageAdmin(admin.StackedInline):
    model = AdventureTourImage


@admin.register(AdventureTour)
class AdventureTourAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'duration_days', 'price')
    search_fields = ('name', 'location')
    inlines = [AdventureTourImageAdmin]


class ComboTourImageAdmin(admin.StackedInline):
    model = ComboTourImage


@admin.register(ComboTour)
class ComboTourAdmin(admin.ModelAdmin):
    list_display = ('name', 'theme_park', 'price')
    search_fields = ('name', 'theme_park__name')
    inlines = [ComboTourImageAdmin]


class DubaiActivityImageAdmin(admin.StackedInline):
    model = DubaiActivityImage


@admin.register(DubaiActivity)
class DubaiActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'duration_hours',
                    'age_limit', 'includes_meals')
    search_fields = ('name', 'location')
    inlines = [DubaiActivityImageAdmin]


@admin.register(ThemeParkReservation)
class ThemeParkReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme_park', 'admission_count',
                    'status', 'reservation_date')
    list_filter = ('theme_park', 'status', 'reservation_date')
    search_fields = ('user__email', 'theme_park__name')


@admin.register(TopAttractionReservation)
class TopAttractionReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'top_attraction', 'ticket_count',
                    'status', 'reservation_date')
    list_filter = ('top_attraction__theme_park', 'status', 'reservation_date')
    search_fields = ('user__email', 'top_attraction__name')


@admin.register(DesertSafariReservation)
class DesertSafariReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'desert_safari', 'participant_count',
                    'status', 'reservation_date')
    list_filter = ('desert_safari', 'status', 'reservation_date')
    search_fields = ('user__email', 'desert_safari__location')


@admin.register(WaterParkReservation)
class WaterParkReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'water_park', 'admission_count',
                    'status', 'reservation_date')
    list_filter = ('water_park', 'status', 'reservation_date')
    search_fields = ('user__email', 'water_park__name')


@admin.register(WaterActivityReservation)
class WaterActivityReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'water_activity',
                    'participant_count', 'status', 'reservation_date')
    list_filter = ('water_activity__water_park', 'status', 'reservation_date')
    search_fields = ('user__email', 'water_activity__name')


@admin.register(AdventureTourReservation)
class AdventureTourReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'adventure_tour',
                    'participant_count', 'status', 'reservation_date')
    list_filter = ('adventure_tour', 'status', 'reservation_date')
    search_fields = ('user__email', 'adventure_tour__name')


@admin.register(ComboTourReservation)
class ComboTourReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'combo_tour', 'participant_count',
                    'status', 'reservation_date')
    list_filter = ('combo_tour__theme_park', 'status', 'reservation_date')
    search_fields = ('user__email', 'combo_tour__name')


@admin.register(DubaiActivityReservation)
class DubaiActivityReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'dubai_activity',
                    'participant_count', 'status', 'reservation_date')
    list_filter = ('dubai_activity__location', 'status', 'reservation_date')
    search_fields = ('user__email', 'dubai_activity__name')


@admin.register(RefundRequest)
class RefundRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'request_date', 'refund_date')
    list_filter = ('status', 'request_date', 'refund_date')
    search_fields = ('user__email', 'order_id')
    readonly_fields = ('id', 'request_date')

    fieldsets = (
        ('General Information', {
            'fields': ('id', 'user', 'status', 'request_date', 'refund_date')
        }),
        ('Reservation Details', {
            'fields': ('hotel', 'car', 'flight', 'bus', 'package', 'yacht', 'theme_park',
                       'top_attraction', 'desert_safari', 'water_park', 'water_activity',
                       'adventure_tour', 'combo_tour', 'dubai_activity')
        }),
        ('Refund Information', {
            'fields': ('order_id', 'refund_amount')
        }),
    )

# Customer review models


@admin.register(HotelCustomerReview)
class HotelCustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'user', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    search_fields = ('hotel__name', 'user')


@admin.register(CarCustomerReview)
class CarCustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    search_fields = ('car__name', 'user')


@admin.register(FlightCustomerReview)
class FlightCustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('flight', 'user', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    search_fields = ('flight__flight_number', 'user')


@admin.register(PackageCustomerReview)
class PackageCustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('package', 'user', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    search_fields = ('package__name', 'user')


@admin.register(YachtCustomerReview)
class YachtCustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('yacht', 'user', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    search_fields = ('yacht__name', 'user')


@admin.register(ThemeParkCustomerReview)
class ThemeParkCustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('themepark', 'user', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    search_fields = ('themepark__name', 'user')


@admin.register(TopAttractionCustomerReview)
class TopAttractionCustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('topattraction', 'user', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    search_fields = ('topattraction__name', 'user')


@admin.register(DesertSafariCustomerReview)
class DesertSafariCustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('desertsafari', 'user', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    search_fields = ('desertsafari__name', 'user')


@admin.register(WaterParkCustomerReview)
class WaterParkCustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('waterpark', 'user', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    search_fields = ('waterpark__name', 'user')


@admin.register(WaterActivityCustomerReview)
class WaterActivityCustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('wateractivity', 'user', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    search_fields = ('wateractivity__name', 'user')


@admin.register(AdventureTourCustomerReview)
class AdventureTourCustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('adventuretour', 'user', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    search_fields = ('adventuretour__name', 'user')


@admin.register(ComboTourCustomerReview)
class ComboTourCustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('combotour', 'user', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    search_fields = ('combotour__name', 'user')


@admin.register(DubaiActivityCustomerReview)
class DubaiActivityCustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('dubaiactivity', 'user', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    search_fields = ('dubaiactivity__name', 'user')


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')
    list_filter = ('theme_park', 'top_attraction', 'desert_safari', 'water_park',
                   'water_activity', 'adventure_tour', 'combo_tour', 'dubai_activity')
    ordering = ('-id',)


@admin.register(SelfDriveRental)
class SelfDriveRentalAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'name', 'email', 'phone_number', 'from_date', 'to_date',
                    'driver_license_number', 'from_location', 'to_location', 'notes', 'total_rental_days')
    list_filter = ('car', 'from_date', 'to_date')
    search_fields = ('car', 'name', 'email', 'driver_license_number')



class CityTourImageInline(admin.TabularInline):
    model = CityTourImage

@admin.register(CityTour)
class CityTourAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'price')
    inlines = [CityTourImageInline]