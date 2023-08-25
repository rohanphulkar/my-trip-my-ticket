from django.urls import path
from . import views
urlpatterns = [
    path('bookings/', views.BookingListView.as_view(), name='booking-list'),
    path('bookings/<uuid:pk>/', views.BookingDetailsView.as_view(), name='booking-detail'),
    path("booking/cancel/<uuid:booking_id>/", views.BookingCancelView.as_view(), name="booking_cencel"),
    path('hotels/', views.HotelListView.as_view(), name='hotel-list'),
    path('hotels/<uuid:pk>/', views.HotelDetailsView.as_view(), name='hotel-detail'),
    path('cars/', views.CarListView.as_view(), name='car-list'),
    path('cars/<uuid:pk>/', views.CarDetailsView.as_view(), name='car-detail'),
    path('airports/', views.AirportListView.as_view(), name='airport-list'),
    path('airports/<int:pk>/', views.AirportDetailsView.as_view(), name='airport-detail'),
    path('flights/', views.FlightListView.as_view(), name='flight-list'),
    path('flights/<int:pk>/', views.FlightDetailsView.as_view(), name='flight-detail'),
    path('buses/', views.BusListView.as_view(), name='bus-list'),
    path('buses/<uuid:pk>/', views.BusDetailsView.as_view(), name='bus-detail'),
    path('offers/', views.OfferListView.as_view(), name='offer-list'),
    path('offers/<uuid:pk>/', views.OfferDetailsView.as_view(), name='offer-detail'),
    path("payment/", views.PaymentView.as_view(), name="payment"),
    path("payment-confirm/", views.PaymentConfirmationView.as_view(), name="payment_confirmation"),
]
