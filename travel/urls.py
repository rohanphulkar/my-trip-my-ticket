from django.urls import path
from .views import *
urlpatterns = [
    path("tours/", ToursView.as_view(), name="tours"),
    path("adimages/", AdImageView.as_view(), name="adimages"),
    path("itineraries/", UserItineraryView.as_view(), name="itineraries"),
    path("itineraries/<id>/", UserItineraryView.as_view(), name="itinerary_details"),
    path("bookings/", BookingView.as_view(), name="bookings"),
    path("bookings/<id>/", BookingView.as_view(), name="booking_details"),
]
