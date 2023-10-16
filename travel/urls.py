from django.urls import path
from . import views
urlpatterns = [
    path('adimages/', views.AdImageView.as_view(), name='adimages'),
    path('bookings/', views.BookingListView.as_view(), name='booking-list'),
    path('bookings/user/', views.UserBookingsView.as_view(), name='user-bookings'),
    path('bookings/<pk>/', views.BookingDetailsView.as_view(), name='booking-detail'),
    path("booking/cancel/<pk>/", views.BookingCancelView.as_view(), name="booking_cencel"),
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
    path('yachts/', views.YachtList.as_view(), name='yacht-list'),
    path('yachts/<uuid:pk>/', views.YachtDetail.as_view(), name='yacht-detail'),
    path('offers/', views.OfferListView.as_view(), name='offer-list'),
    path('offers/<uuid:pk>/', views.OfferDetailsView.as_view(), name='offer-detail'),
    path('check-offer/<code>/',views.CheckOfferView.as_view(),name='check_offer'),
    path('packages/', views.PackageListView.as_view(), name='package-list'),
    path('packages/<uuid:pk>/', views.PackageDetailsView.as_view(), name='package-detail'),
    path("payment/", views.PaymentView.as_view(), name="payment"),
    path("payment-confirm/", views.PaymentConfirmationView, name="payment_confirmation"),
    path('contact/', views.ContactAPIView.as_view(), name='contact'),
    path('theme-parks/', views.ThemeParkList.as_view(), name='theme-park-list'),
    path('top-attractions/', views.TopAttractionList.as_view(), name='top-attraction-list'),
    path('desert-safaris/', views.DesertSafariList.as_view(), name='desert-safari-list'),
    path('water-parks/', views.WaterParkList.as_view(), name='water-park-list'),
    path('water-activities/', views.WaterActivityList.as_view(), name='water-activity-list'),
    path('adventure-tours/', views.AdventureTourList.as_view(), name='adventure-tour-list'),
    path('combo-tours/', views.ComboTourList.as_view(), name='combo-tour-list'),
    path('dubai-activities/', views.DubaiActivityList.as_view(), name='dubai-activity-list'),
    path("duplicate/", views.duplicate_instance, name="duplicate_instance"),
    path('get_model_instances/', views.get_model_instances, name='get_model_instances'),
    path('forex/create/', views.ForexCreateView.as_view(), name='forex-create'),
    path("visa/", views.VisaCreateView.as_view(), name="visa"),
    path("review/create/<model>/<object_id>/", views.CustomerReviewView.as_view(), name="customer_review")
]
