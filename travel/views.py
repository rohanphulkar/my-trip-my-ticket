from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework import status,filters, generics
from rest_framework.response import Response
from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TourPriceFilter
from decouple import config
import razorpay
import json
from .helper import send_booking_confirmation_email,send_booking_cancellation_email

client = razorpay.Client(auth=(config('RZP_KEY'), config('RZP_SECRET')))

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
    filterset_fields = ['user', 'tour','hotel','car', 'status']
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
        
        
        try:
            payment = client.order.create({
                "amount":int(package_instance.price * 100),
                "currency":"INR",
                "payment_capture":"1"
            })
            
            booking = Booking.objects.create(
                user = user,
                tour=None if package_type != 'tour' else package_instance,
                hotel=None if package_type != 'hotel' else package_instance,
                car=None if package_type != 'car' else package_instance,
                payment_amount = package_instance.price,
                payment_id = payment['id']
            )

            serializer = BookingSerializer(booking,many=False)

            data = {
                'payment':payment,
                "booking":serializer.data
            }
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

class PaymentConfirmationView(APIView):
    def post(self,request):
        try:
            res = json.loads(request.data['response'])
            
            global ord_id
            global raz_pay_id
            global raz_signature

            for key in res.keys():
                if key == 'razorpay_order_id':
                    ord_id = res[key]
                elif key == 'razorpay_payment_id':
                    raz_pay_id = res[key]
                elif key == 'razorpay_signature':
                    raz_signature = res[key]
            
            booking = Booking.objects.get(payment_id=ord_id)

            data = {
                'razorpay_order_id':ord_id,
                'razorpay_payment_id':raz_pay_id,
                'razorpay_signature':raz_signature
            }
            
            def verify_signature(data):
                return client.utility.verify_payment_signature(data)
            
            if not verify_signature(data):
                booking.status = 'failed'
                booking.payment_status = 'failed'
                booking.save()
                return Response({'error':'payment failed'},status=status.HTTP_400_BAD_REQUEST)

            booking.status = 'confirmed'
            booking.payment_status = 'paid'
            booking.save()

            context = {
                'email':booking.user.email,
                'id':booking.id,
                'date':booking.booking_date,
                'amount':booking.payment_amount
            }

            email_sent = send_booking_confirmation_email(context)
            return Response({'message':'your booking has been confirmed.'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

class BookingCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,booking_id):
        try:
            booking = Booking.objects.filter(id=booking_id,user=request.user).first()
            if booking.status == 'cancelled':
                return Response({'message': 'Booking is already cancelled'}, status=status.HTTP_400_BAD_REQUEST)

            refund_amount = int(booking.payment_amount * 100)

            refund_data = {
                'payment_id':booking.payment_id,
                'amount':refund_amount,
                'currency':'INR'
            }

            refund = client.payment.refund.create(data=refund_data)

            if refund.get('error_code') is not None:
                return Response({'error': 'Refund not successful'}, status=status.HTTP_400_BAD_REQUEST)
            
            booking.status = 'cancelled'
            booking.save()

            context = {
                'email':booking.user.email,
                'id':booking.id,
                'date':booking.booking_date,
                'amount':booking.payment_amount
            }
            email_sent = send_booking_cancellation_email(context)
            return Response({'message': 'Booking cancelled and refund initiated'},status=status.HTTP_200_OK)
        
        except Booking.DoesNotExist:
            return Response({'error':'Booking not found'},status=status.HTTP_404_NOT_FOUND)    