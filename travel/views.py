from django.shortcuts import redirect,render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework import status,filters, generics
from rest_framework.response import Response
from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from decouple import config
import razorpay
from .helper import send_booking_confirmation_email,send_booking_cancellation_email,save_pdf
from datetime import date
from .filters import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import date,datetime
from django.core.files.base import ContentFile
client = razorpay.Client(auth=(config('RZP_KEY'), config('RZP_SECRET')))



class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['booking_date', 'check_in_date', 'check_out_date']
    filterset_class = BookingFilter
    filter_fields = ["status"]
    
# class UserBookingsView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         bookings = Booking.objects.filter(user=request.user)
#         serializer = BookingSerializer(bookings, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

class UserBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = []  # Add any search fields if needed
    ordering_fields = ['created_at']  # Add fields to allow ordering if needed

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BookingDetailsView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class HotelListView(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter,DjangoFilterBackend]
    filterset_class = HotelFilter
    filter_fields = ['city', 'pin', 'star_category', 'amenities', 'tax_type', 'tax_percent_min', 'tax_percent_max', 'total_rooms_min', 'total_rooms_max', 'available_rooms_min', 'available_rooms_max', 'price_min', 'price_max', 'available_from_after', 'available_from_before', 'available_to_after', 'available_to_before']

class HotelDetailsView(generics.RetrieveAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class CarListView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter,DjangoFilterBackend]
    filterset_class = CarFilter
    filter_fields = ['car_type', 'fuel_type', 'seats_min', 'seats_max', 'transmission', 'ac', 'bags', 'price_min', 'price_max', 'origin_city', 'destination_city', 'available_from_after', 'available_from_before']

class CarDetailsView(generics.RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class AdImageView(generics.ListAPIView):
    queryset = AdImage.objects.all()
    serializer_class = AdImageSerializer

class AirportListView(generics.ListAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'name', 'city', 'country']
    filterset_fields = ['code', 'city', 'country']

class AirportDetailsView(generics.RetrieveAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

class FlightListView(generics.ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = FlightFilter
    filter_fields = ['departure_airport_city', 'arrival_airport_city', 'departure_time_after', 'departure_time_before', 'arrival_time_after', 'arrival_time_before', 'available_seats_min', 'available_seats_max', 'price_min', 'price_max']

class FlightDetailsView(generics.RetrieveAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class BusListView(generics.ListAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    filterset_class = BusFilter
    filter_fields = ['departure_station', 'arrival_station', 'departure_date_after', 'departure_date_before', 'departure_time_after', 'departure_time_before', 'arrival_date_after', 'arrival_date_before', 'arrival_time_after', 'arrival_time_before']

class BusDetailsView(generics.RetrieveAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class PackageListView(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PackageFilter
    filter_fields = ['origin_city', 'destination_city', 'activities', 'departure_after', 'departure_before', 'star_category', 'price_min', 'price_max', 'with_flights', 'total_rooms']

class PackageDetailsView(generics.RetrieveAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

class OfferListView(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'description', 'discount_percent']
    filterset_fields = ['code']
    
class OfferDetailsView(generics.RetrieveAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

class CheckOfferView(APIView):
    def get(self,request,code):
        try:
            offer = Offer.objects.get(code=code)
        except Exception as e:
            return Response({'error':'Offer Code is invalid'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = OfferSerializer(offer,many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)



class PaymentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        package_type = request.data.get('package_type',None)
        user = request.user
        user_obj = {'name':user.name,"email":user.email,'phone':user.phone}
        promo_code = request.data.get('promo_code',None)
        people = request.data.get('people',1)
        package_id = request.data.get('package_id',None)
        contact_email = request.data.get('email',None)
        contact_phone = request.data.get('phone',None)
        startDate = request.data.get('start_date',None)
        endDate = request.data.get('end_date',None)

        if package_type == 'hotel':
            try:
                room = Room.objects.get(id=package_id)
            except Room.DoesNotExist:
                return Response({'error':'Invalid package id'},status=status.HTTP_404_NOT_FOUND)

            if room.available_rooms<=0 or not room.availability:
                return Response({'error':'Room is not available'},status=status.HTTP_400_BAD_REQUEST)
            reservation = HotelReservation.objects.create(user=user,hotel=room.hotel,room=room,total_guests=people,check_in_date=startDate,check_out_date=endDate,contact_email=contact_email,contact_phone=contact_phone)

            amount = room.price * int(people)


        elif package_type == 'car':
            try:
                car = Car.objects.get(id=package_id)
            except Car.DoesNotExist:
                return Response({'error':'Invalid package id'},status=status.HTTP_404_NOT_FOUND)
            if car.available_cars <=0:
                return Response({'error':'Car is not available'},status=status.HTTP_400_BAD_REQUEST)
            reservation = CarReservation.objects.create(user=user,car=car,passenger=people,contact_email=contact_email,contact_phone=contact_phone,rental_start_date=startDate,rental_end_date=endDate)
            amount = car.price * int(people)
        elif package_type == 'flight':
            try:
                flight = Flight.objects.get(id=package_id)
            except Flight.DoesNotExist:
                return Response({'error':'Invalid package id'},status=status.HTTP_404_NOT_FOUND)
            if flight.available_seats <=0:
                return Response({'error':'Flight is not available'},status=status.HTTP_400_BAD_REQUEST)
         
            reservation = FlightReservation.objects.create(user=user,flight=flight,passenger=people,contact_email=contact_email,contact_phone=contact_phone,departure_on=startDate)
            amount = flight.price * int(people)
        elif package_type == 'bus':
            try:
                bus = Bus.objects.get(id=package_id)
            except Bus.DoesNotExist:
                return Response({'error':'Invalid package id'},status=status.HTTP_404_NOT_FOUND)
            if bus.available_seats <=0:
                return Response({'error':'No seats available'},status=status.HTTP_400_BAD_REQUEST)
            
            reservation = BusReservation.objects.create(user=user,bus=bus,passenger=people,contact_email=contact_email,contact_phone=contact_phone,departure_on=startDate)
            amount = bus.price * int(people)
            
        elif package_type == 'package':
            try:
                package = Package.objects.get(id=package_id)
            except Package.DoesNotExist:
                return Response({'error':'Invalid package id'},status=status.HTTP_404_NOT_FOUND)
            reservation = PackageReservation.objects.create(user=user,package=package,passenger=people)
            amount = package.price * int(people)
        else:
            return Response({'error': 'Invalid booking type'}, status=status.HTTP_400_BAD_REQUEST)
    
        if promo_code:
            try:
                offer = Offer.objects.get(code=promo_code)
                
                if date.today()> offer.end_date:
                    return Response({'error':'promo code is expired'},status=status.HTTP_400_BAD_REQUEST)
                discount_factor = 1 - offer.discount_percent / 100
                amount = amount * discount_factor
            except Exception as e:
                return Response({'error':'Promo code is invalid'},status=status.HTTP_404_NOT_FOUND)
        
        try:
            payment = client.order.create({
                "amount":int(amount * 100),
                "currency":"INR",
                "payment_capture":"1"
            })

            booking = Booking.objects.create(
                user = user,
                package=reservation if package_type == 'package' else None,
                hotel=reservation if package_type == 'hotel' else None,
                car=reservation if package_type == 'car' else None,
                flight=reservation if package_type == 'flight' else None,
                bus=reservation if package_type == 'bus' else None,
                payment_amount = amount,
                order_id = payment['id']
            )
            
            serializer = PaymentSerializer(booking,many=False)

            data = {
                'payment':payment,
                "booking":serializer.data,
                "user":user_obj
            }
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        


class PaymentConfirmationView(APIView):
    def post(self,request):
        try:
            res = request.data['response']

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
            
            booking = Booking.objects.get(order_id=ord_id)
            

            data = {
                'razorpay_order_id':ord_id,
                'razorpay_payment_id':raz_pay_id,
                'razorpay_signature':raz_signature
            }
            
            if booking.status=='confirmed':
                return Response({'message':'your booking has already been confirmed.'},status=status.HTTP_200_OK)
            
            def verify_signature(data):
                return client.utility.verify_payment_signature(data)
            
            if not verify_signature(data):
                booking.status = 'failed'
                booking.payment_status = 'failed'
                booking.save()
                return Response({'error':'payment failed'},status=status.HTTP_400_BAD_REQUEST)

            booking.status = 'confirmed'
            booking.payment_status = 'paid'
            booking.payment_id = raz_pay_id
            booking.save()
            if booking.hotel:
                hotel = HotelReservation.objects.get(id=booking.hotel.id)
                hotel.status = 'confirmed'
                hotel.room.available_rooms -=  1
                hotel.room.save()
                email = hotel.contact_email
                phone = hotel.contact_phone
                from_city = hotel.hotel.city
                to_city = None
                start_date = hotel.check_in_date
                end_date = hotel.check_out_date
                people = hotel.total_guests
                hotel.save()
            elif booking.car:
                car = CarReservation.objects.get(id=booking.car.id)
                car.status = 'confirmed'
                car.car.available_cars -= 1
                car.car.save()
                email = car.contact_email
                phone = car.contact_phone
                start_date = car.rental_start_date
                end_date = car.rental_end_date
                people = car.passenger
                from_city = car.car.origin_city
                to_city = car.car.destination_city
                car.save()
            elif booking.flight:
                flight = FlightReservation.objects.get(id=booking.flight.id)
                flight.status = 'confirmed'
                flight.flight.available_seats -= 1
                flight.flight.save()
                email = flight.contact_email
                phone = flight.contact_phone
                start_date = flight.departure_on
                end_date = None
                people = flight.passenger
                from_city = flight.flight.departure_airport.city
                to_city = flight.flight.arrival_airport.city
                flight.save()
            elif booking.bus:
                bus = BusReservation.objects.get(id=booking.bus.id)
                bus.status = 'confirmed'
                bus.bus.available_seats -= 1
                bus.bus.save()
                email = bus.contact_email
                phone = bus.contact_phone
                start_date = bus.departure_on
                end_date = None
                people = bus.passenger
                from_city = bus.bus.departure_station
                to_city = bus.bus.arrival_station
                bus.save()
            elif booking.package:
                package = PackageReservation.objects.get(id=booking.package.id)
                package.status = 'confirmed'
                email = package.contact_email
                phone = package.contact_phone
                start_date = None
                end_date = None
                people = package.passenger
                from_city = package.package.origin_city
                to_city = package.package.destination_city
                package.save()


            context = {
                'email':email,
                'id':booking.id,
                'date':booking.booking_date,
                'amount':booking.payment_amount
            }
            pdf_params = {
                'booking_id':booking.id,
                'booking_date':datetime.strptime(str(booking.booking_date), "%Y-%m-%d %H:%M:%S.%f%z").strftime("%d %B %Y"),
                "email": email,
                "phone": phone,
                "make": car.car.make if booking.car else None,
                "model": car.car.model if booking.car else None,
                "hotel_name": hotel.hotel.name if booking.hotel else None,
                "hotel_city": hotel.hotel.city if booking.hotel else None,
                "room_type": hotel.room.room_type if booking.hotel else None,
                "flight_number": flight.flight.flight_number if booking.flight else None,
                "flight_name": flight.flight.name if booking.flight else None,
                "bus_number": bus.bus.bus_number if booking.bus else None,
                "bus_type": bus.bus.bus_type if booking.bus else None,
                "bus_operator": bus.bus.operator if booking.bus else None,
                "people": people,
                "from": from_city,
                "to": to_city,
                "start_date": datetime.strptime(str(start_date), "%Y-%m-%d").strftime("%d %B %Y"),
                "end_date": datetime.strptime(str(end_date), "%Y-%m-%d").strftime("%d %B %Y")
            }

            email_sent = send_booking_confirmation_email(context)

            pdf_content = save_pdf(pdf_params)
            booking.pdf.save(f'{uuid.uuid4()}.pdf',ContentFile(pdf_content))

            return Response({'message':'your booking has been confirmed.'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

class BookingCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        try:
            booking = Booking.objects.filter(pk=pk,user=request.user).first()
            if booking.status == 'cancelled':
                return Response({'message': 'Booking is already cancelled'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                refund_amount = int(booking.payment_amount * 100)

                refund_data = {
                    'amount':refund_amount,
                    'currency':'INR',
                    'speed':'normal'
                }

                refund = client.payment.refund(booking.payment_id,refund_data)

                if refund.get('error_code') is not None:
                    return Response({'error': 'Refund not successful'}, status=status.HTTP_400_BAD_REQUEST)
                
                booking.status = 'cancelled'
                booking.save()

                if booking.hotel:
                    hotel = HotelReservation.objects.get(id=booking.hotel.id)
                    hotel.status = 'cancelled'
                    hotel.room.available_rooms +=  1
                    hotel.room.save()
                    email = hotel.contact_email
                    hotel.save()
                elif booking.car:
                    car = CarReservation.objects.get(id=booking.car.id)
                    car.status = 'cancelled'
                    car.car.available_cars += 1
                    car.car.save()
                    email = car.contact_email
                    car.save()
                elif booking.flight:
                    flight = FlightReservation.objects.get(id=booking.flight.id)
                    flight.status = 'cancelled'
                    flight.flight.available_seats += 1
                    flight.flight.save()
                    email = flight.contact_email
                    flight.save()
                elif booking.bus:
                    bus = BusReservation.objects.get(id=booking.bus.id)
                    bus.status = 'cancelled'
                    bus.bus.available_seats += 1
                    bus.bus.save()
                    email = bus.contact_email
                    bus.save()
                elif booking.package:
                    package = PackageReservation.objects.get(id=booking.package.id)
                    package.status = 'cancelled'
                    email = package.contact_email
                    package.save()

                context = {
                    'email':email,
                    'id':booking.id,
                    'date':booking.booking_date,
                    'amount':booking.payment_amount
                }
                email_sent = send_booking_cancellation_email(context)
                return Response({'message': 'Booking cancelled and refund initiated'},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        except Booking.DoesNotExist:
            return Response({'error':'Booking not found'},status=status.HTTP_404_NOT_FOUND)

class ContactAPIView(APIView):
    def post(self, request, format=None):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            phone_number = serializer.validated_data['phone_number']
            message = serializer.validated_data['message']

            send_mail(
                'Contact Form Submission',
                f'You have a new contact form submission from:\n\nName: {name}\nEmail: {email}\nPhone Number: {phone_number}\n\nMessage: {message}',
                settings.EMAIL_HOST_USER,
                [config('EMAIL_RECEPIENT_USER')],
                fail_silently=False,
            )

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ForexCreateView(generics.CreateAPIView):
    queryset = Forex.objects.all()
    serializer_class = ForexCreateSerializer
class VisaCreateView(generics.CreateAPIView):
    queryset = Visa.objects.all()
    serializer_class = VisaCreateSerializer

from django.apps import apps
import uuid
from django.http import JsonResponse

def get_model_instances(request):
    model_name = request.GET.get('model_name')
    selected_model = apps.get_model(app_label='travel', model_name=model_name)
    instances = selected_model.objects.all() if selected_model else []

    instance_data = [{'pk': instance.pk, 'str': str(instance)} for instance in instances]

    return JsonResponse({'instances': instance_data})


@csrf_exempt
def duplicate_instance(request):
    models_list = apps.all_models['travel']

    if request.method =='POST':

        model = request.POST.get('model',None)
        inst = request.POST.get('instance',None)
        count = request.POST.get('count',1)
        if not model:
            messages.error(request,"Please select a model.")
        if not inst:
            messages.error(request,"Please select a instance.")
        
        model = apps.get_model(app_label='travel',model_name=model)

        instance = model.objects.get(pk=inst)
        data = vars(instance)
        data.pop("_state")
        for i in range(int(count)):
            data.update({"id":uuid.uuid4()})
            new_instance = model(**data)
            new_instance.save()
        messages.success(request,f"{count} entries of {instance} has been created.")
    return render(request,'travel/duplicate_instance.html',{'model_list':dict(models_list.items())})
    


class DubaiActivityList(generics.ListAPIView):
    queryset = DubaiActivity.objects.all()
    serializer_class = DubaiActivitySerializer

class DubaiActivityDetail(generics.RetrieveAPIView):
    queryset = DubaiActivity.objects.all()
    serializer_class = DubaiActivitySerializer
