from django.urls import path
from . import views
urlpatterns = [
    path('tours/', views.TourListView.as_view(), name='tour-list'),
    path('tours/<uuid:pk>/', views.TourDetailsView.as_view(), name='tour-detail'),
    path('bookings/', views.BookingListView.as_view(), name='booking-list'),
    path('bookings/<uuid:pk>/', views.BookingDetailsView.as_view(), name='booking-detail'),
    path("booking/cancel/<uuid:booking_id>/", views.BookingCancelView.as_view(), name="booking_cencel"),
    path('hotels/', views.HotelListView.as_view(), name='hotel-list'),
    path('hotels/<uuid:pk>/', views.HotelDetailsView.as_view(), name='hotel-detail'),
    path('cars/', views.CarListView.as_view(), name='car-list'),
    path('cars/<uuid:pk>/', views.CarDetailsView.as_view(), name='car-detail'),
    path('user-itineraries/', views.UserItineraryListView.as_view(), name='user-itinerary-list'),
    path('user-itineraries/<uuid:pk>/', views.UserItineraryDetailsView.as_view(), name='user-itinerary-detail'),
    path("payment/", views.PaymentView.as_view(), name="payment"),
    path("payment-confirm/", views.PaymentConfirmationView.as_view(), name="payment_confirmation"),

]
