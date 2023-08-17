from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework import status,filters, generics
from rest_framework.response import Response
from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TourPriceFilter
import stripe
from decouple import config
from django.conf import settings
from django.core.mail import send_mail
stripe.api_key = config('STRIPE_SECRET_KEY')

class TourListView(generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'location']
    filter_class = TourPriceFilter
    filterset_fields = ['price']
    ordering_fields = ['title', 'price']
    

class TourDetailsView(generics.RetrieveAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'tour', 'status']
    ordering_fields = ['booking_date', 'check_in_date', 'check_out_date']

class BookingDetailsView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

class HotelListView(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'country', 'state', 'city']
    ordering_fields = ['name', 'star_category', 'rent']

class HotelDetailsView(generics.RetrieveAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class CarListView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'country', 'state', 'city', 'make', 'model']
    ordering_fields = ['name', 'passengers', 'rent']

class CarDetailsView(generics.RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer



class AdImageView(generics.ListAPIView):
    queryset = AdImage.objects.all()
    serializer_class = AdImageSerializer


class UserItineraryListView(generics.ListAPIView):
    serializer_class = UserItinerarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserItinerary.objects.filter(user=self.request.user)

class UserItineraryDetailsView(generics.RetrieveAPIView):
    queryset = UserItinerary.objects.all()
    serializer_class = UserItinerarySerializer
    permission_classes = [IsAuthenticated]


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        package_type = request.data.get('package_type',None)
        package_id = request.data.get('package_id',None)
        user = request.user

        if package_type =='tour':
            package_model = Tour
        elif package_type == 'hotel':
            package_model = Hotel
        elif package_type == 'car':
            package_model = Car
        else:
            return Response({'error': 'Invalid booking type'}, status=status.HTTP_400_BAD_REQUEST) 
        
        try:
            package_instance = package_model.objects.get(pk=package_id)
        except package_model.DoesNotExist:
            return Response({'error': 'Package not found'}, status=status.HTTP_404_NOT_FOUND)
        
        booking = Booking.objects.create(
            user = user,
            tour=None if package_type != 'tour' else package_instance,
            hotel=None if package_type != 'hotel' else package_instance,
            car=None if package_type != 'car' else package_instance,
            payment_amount = package_instance.price
        )

        try:

            session = stripe.checkout.Session.create(
                success_url = settings.FRONTEND_URL + '/success',
                cancel_url = settings.FRONTEND_URL + '/cancel',
                payment_method_types = ['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'inr',
                            'unit_amount': int(booking.payment_amount * 100),  # Amount in cents
                            'product_data': {
                                'name': f'Booking #{booking.id}',
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
            )

            booking.payment_id = session.id
            booking.save()

            return redirect(session.url,status=status.HTTP_303_SEE_OTHER)
        except Exception as e:
            return Response({'error':e},status=status.HTTP_400_BAD_REQUEST)

class PaymentConfirmationView(APIView):
    def post(self,request):
        payment_id = request.data.get('payment_id')

        try:
            booking = Booking.objects.get(payment_id=payment_id)
        except Booking.DoesNotExist:
            return Response({'error':'Booking not found'},status=status.HTTP_404_NOT_FOUND)
        
        try:
            session = stripe.checkout.Session.retrieve(payment_id)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
        if session.payment_status == 'paid':
            booking.status =='confirmed'
            booking.payment_status=='paid'
            booking.save()

            subject = 'Booking Confirmation'
            message = 'Your booking has been confirmed and payment is successful.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [booking.user.email]
            send_mail(subject, message, from_email, recipient_list)

            return Response({'message':'payment successful.'},status=status.HTTP_200_OK)
        else:
            booking.status = 'failed'
            booking.payment_status = 'failed'
            booking.save()

            return Response({'error':'payment failed'},status=status.HTTP_400_BAD_REQUEST)

class BookingCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,booking_id):
        try:
            booking = Booking.objects.filter(id=booking_id,user=request.user).first()
            booking.status = 'cancelled'
            booking.save()
            return Response({'message':'booking cancelled successfully'},status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({'error':'Booking not found'},status=status.HTTP_404_NOT_FOUND)      