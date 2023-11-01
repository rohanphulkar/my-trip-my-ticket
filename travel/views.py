from django.shortcuts import redirect,render,HttpResponse,get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework import status,filters, generics
from rest_framework.response import Response
from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from decouple import config
from .helper import send_booking_confirmation_email,send_booking_cancellation_email,save_pdf
from datetime import date
from .filters import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import date,datetime
from django.core.files.base import ContentFile
from .ccavutil import encrypt,decrypt
from .ccavResponseHandler import res
from string import Template
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from shortuuid import ShortUUID

accessCode=config('ACCESS_KEY')
workingKey = config('WORKING_KEY')
merchantId= config('MERCHANT_ID')


class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['booking_date', 'check_in_date', 'check_out_date']
    filterset_class = BookingFilter
    filter_fields = ["status"]
    


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

class YachtList(generics.ListAPIView):
    queryset = Yacht.objects.all()
    serializer_class = YachtSerializer

class YachtDetail(generics.RetrieveAPIView):
    queryset = Yacht.objects.all()
    serializer_class = YachtSerializer


class ThemeParkList(generics.ListAPIView):
    queryset = ThemePark.objects.all()
    serializer_class = ThemeParkSerializer

class TopAttractionList(generics.ListAPIView):
    queryset = TopAttraction.objects.all()
    serializer_class = TopAttractionSerializer

class DesertSafariList(generics.ListAPIView):
    queryset = DesertSafari.objects.all()
    serializer_class = DesertSafariSerializer

class WaterParkList(generics.ListAPIView):
    queryset = WaterPark.objects.all()
    serializer_class = WaterParkSerializer

class WaterActivityList(generics.ListAPIView):
    queryset = WaterActivity.objects.all()
    serializer_class = WaterActivitySerializer

class AdventureTourList(generics.ListAPIView):
    queryset = AdventureTour.objects.all()
    serializer_class = AdventureTourSerializer

class ComboTourList(generics.ListAPIView):
    queryset = ComboTour.objects.all()
    serializer_class = ComboTourSerializer

class DubaiActivityList(generics.ListAPIView):
    queryset = DubaiActivity.objects.all()
    serializer_class = DubaiActivitySerializer


class ThemeParkDetail(generics.RetrieveAPIView):
    queryset = ThemePark.objects.all()
    serializer_class = ThemeParkSerializer

class TopAttractionDetail(generics.RetrieveAPIView):
    queryset = TopAttraction.objects.all()
    serializer_class = TopAttractionSerializer

class DesertSafariDetail(generics.RetrieveAPIView):
    queryset = DesertSafari.objects.all()
    serializer_class = DesertSafariSerializer

class WaterParkDetail(generics.RetrieveAPIView):
    queryset = WaterPark.objects.all()
    serializer_class = WaterParkSerializer

class WaterActivityDetail(generics.RetrieveAPIView):
    queryset = WaterActivity.objects.all()
    serializer_class = WaterActivitySerializer

class AdventureTourDetail(generics.RetrieveAPIView):
    queryset = AdventureTour.objects.all()
    serializer_class = AdventureTourSerializer

class ComboTourDetail(generics.RetrieveAPIView):
    queryset = ComboTour.objects.all()
    serializer_class = ComboTourSerializer

class DubaiActivityDetail(generics.RetrieveAPIView):
    queryset = DubaiActivity.objects.all()
    serializer_class = DubaiActivitySerializer

class CityTourList(generics.ListAPIView):
    queryset = CityTour.objects.all()
    serializer_class = CityTourSerializer

class CityTourDetail(generics.RetrieveAPIView):
    queryset = CityTour.objects.all()
    serializer_class = CityTourSerializer

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
        promo_code = request.data.get('promo_code','')
        people = request.data.get('people',1)
        package_id = request.data.get('package_id',None)
        contact_email = request.data.get('email',None)
        contact_phone = request.data.get('phone',None)
        startDate = request.data.get('start_date',None)
        endDate = request.data.get('end_date','')

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
            reservation = PackageReservation.objects.create(user=user,package=package,passenger=people,contact_email=contact_email,contact_phone=contact_phone)
            amount = package.price * int(people)
            
        elif package_type == 'yacht':
            try:
                package = Yacht.objects.get(id=package_id)
            except Package.DoesNotExist:
                return Response({'error':'Invalid package id'},status=status.HTTP_404_NOT_FOUND)
            reservation = YachtReservation.objects.create(user=user,yacht=package,passenger=people,contact_email=contact_email,contact_phone=contact_phone)
            amount = package.charter_price * int(people)
        elif package_type == 'theme-park':
            try:
                package = ThemePark.objects.get(id=package_id)
            except Package.DoesNotExist:
                return Response({'error':'Invalid package id'},status=status.HTTP_404_NOT_FOUND)
            reservation = ThemeParkReservation.objects.create(user=user,theme_park=package,admission_count=people,contact_email=contact_email,contact_phone=contact_phone)
            amount = package.price * int(people)
        elif package_type == 'top-attraction':
            try:
                package = TopAttraction.objects.get(id=package_id)
            except Package.DoesNotExist:
                return Response({'error':'Invalid package id'},status=status.HTTP_404_NOT_FOUND)
            reservation = TopAttractionReservation.objects.create(user=user,top_attraction=package,ticket_count=people,contact_email=contact_email,contact_phone=contact_phone)
            amount = package.price * int(people)
        elif package_type == 'desert-safari':
            try:
                package = DesertSafari.objects.get(id=package_id)
            except Package.DoesNotExist:
                return Response({'error':'Invalid package id'},status=status.HTTP_404_NOT_FOUND)
            reservation = DesertSafariReservation.objects.create(user=user,desert_safari=package,participant_count=people,contact_email=contact_email,contact_phone=contact_phone)
            amount = package.price * int(people)
        elif package_type == 'water-park':
            try:
                package = WaterPark.objects.get(id=package_id)
            except Package.DoesNotExist:
                return Response({'error':'Invalid package id'},status=status.HTTP_404_NOT_FOUND)
            reservation = WaterParkReservation.objects.create(user=user,water_park=package,admission_count=people,contact_email=contact_email,contact_phone=contact_phone)
            amount = package.price * int(people)
        elif package_type == 'water-activity':
            try:
                package = WaterActivity.objects.get(id=package_id)
            except Package.DoesNotExist:
                return Response({'error':'Invalid package id'},status=status.HTTP_404_NOT_FOUND)
            reservation = WaterActivityReservation.objects.create(user=user,water_activity=package,participant_count=people,contact_email=contact_email,contact_phone=contact_phone)
            amount = package.price * int(people)
        elif package_type == 'adventure-tour':
            try:
                package = AdventureTour.objects.get(id=package_id)
            except Package.DoesNotExist:
                return Response({'error':'Invalid package id'},status=status.HTTP_404_NOT_FOUND)
            reservation = AdventureTourReservation.objects.create(user=user,adventure_tour=package,participant_count=people,contact_email=contact_email,contact_phone=contact_phone)
            amount = package.price * int(people)
        elif package_type == 'combo-tour':
            try:
                package = ComboTour.objects.get(id=package_id)
            except Package.DoesNotExist:
                return Response({'error':'Invalid package id'},status=status.HTTP_404_NOT_FOUND)
            reservation = ComboTourReservation.objects.create(user=user,combo_tour=package,participant_count=people,contact_email=contact_email,contact_phone=contact_phone)
            amount = package.price * int(people)
        elif package_type == 'dubai-activity':
            try:
                package = DubaiActivity.objects.get(id=package_id)
            except Package.DoesNotExist:
                return Response({'error':'Invalid package id'},status=status.HTTP_404_NOT_FOUND)
            reservation = DubaiActivityReservation.objects.create(user=user,dubai_activity=package,participant_count=people,contact_email=contact_email,contact_phone=contact_phone)
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
            p_merchant_id = merchantId
            p_order_id = ShortUUID(alphabet='0123456789').random(length=10)
            p_currency = 'INR'
            p_amount = int(amount)
            p_redirect_url = f"http://{request.headers['Host']}{reverse('payment_confirmation')}"
            p_cancel_url = f"http://{request.headers['Host']}{reverse('payment_confirmation')}"
            p_language = request.data.get('language', '')
            p_billing_name = request.data.get('billing_name', 'Rohan Phulkar')
            p_billing_address = request.data.get('billing_address', 'mali mohalla')
            p_billing_city = request.data.get('billing_city', 'Maheshwar')
            p_billing_state = request.data.get('billing_state', 'Madhya Pradesh')
            p_billing_zip = request.data.get('billing_zip', '451224')
            p_billing_country = request.data.get('billing_country', 'India')
            p_billing_tel = request.data.get('billing_tel', '7400779162')
            p_billing_email = request.data.get('billing_email', 'rohanphulkar936@gmail.com')
            p_delivery_name = request.data.get('delivery_name', '')
            p_delivery_address = request.data.get('delivery_address', '')
            p_delivery_city = request.data.get('delivery_city', '')
            p_delivery_state = request.data.get('delivery_state', '')
            p_delivery_zip = request.data.get('delivery_zip', '')
            p_delivery_country = request.data.get('delivery_country', '')
            p_delivery_tel = request.data.get('delivery_tel', '')
            p_merchant_param1 = request.data.get('merchant_param1', '')
            p_merchant_param2 = request.data.get('merchant_param2', '')
            p_merchant_param3 = request.data.get('merchant_param3', '')
            p_merchant_param4 = request.data.get('merchant_param4', '')
            p_merchant_param5 = request.data.get('merchant_param5', '')
            p_integration_type = request.data.get('integration_type', '')
            p_promo_code = request.data.get('cc_promo_code', '')
            p_customer_identifier = request.data.get('customer_identifier', '')
            

            merchant_data = (
                f'merchant_id={p_merchant_id}&'
                f'order_id={p_order_id}&'
                f'currency={p_currency}&'
                f'amount={p_amount}&'
                f'redirect_url={p_redirect_url}&'
                f'cancel_url={p_cancel_url}&'
                f'language={p_language}&'
                f'billing_name={p_billing_name}&'
                f'billing_address={p_billing_address}&'
                f'billing_city={p_billing_city}&'
                f'billing_state={p_billing_state}&'
                f'billing_zip={p_billing_zip}&'
                f'billing_country={p_billing_country}&'
                f'billing_tel={p_billing_tel}&'
                f'billing_email={p_billing_email}&'
                f'delivery_name={p_delivery_name}&'
                f'delivery_address={p_delivery_address}&'
                f'delivery_city={p_delivery_city}&'
                f'delivery_state={p_delivery_state}&'
                f'delivery_zip={p_delivery_zip}&'
                f'delivery_country={p_delivery_country}&'
                f'delivery_tel={p_delivery_tel}&'
                f'merchant_param1={p_merchant_param1}&'
                f'merchant_param2={p_merchant_param2}&'
                f'merchant_param3={p_merchant_param3}&'
                f'merchant_param4={p_merchant_param4}&'
                f'merchant_param5={p_merchant_param5}&'
                f'integration_type={p_integration_type}&'
                f'promo_code={p_promo_code}&'
                f'customer_identifier={p_customer_identifier}&'
            )

            encryption = encrypt(merchant_data, workingKey)

            html = '''\
        <html>
        <head>
            <title>Sub-merchant checkout page</title>
            <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
        </head>
        <body>
            <center>
            <!-- width required minimum 482px -->
                <iframe  width="482" height="500" scrolling="No" frameborder="0"  id="paymentFrame" src="https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction&merchant_id=$mid&encRequest=$encReq&access_code=$xscode">
                </iframe>
            </center>

            <script type="text/javascript">
                $(document).ready(function(){
                    $('iframe#paymentFrame').load(function() {
                        window.addEventListener('message', function(e) {
                            $("#paymentFrame").css("height", e.data['newHeight']+'px');
                        }, false);
                    });
                });
            </script>
        </body>
        </html>
        '''


            booking = Booking.objects.create(
                user = user,
                package=reservation if package_type == 'package' else None,
                hotel=reservation if package_type == 'hotel' else None,
                car=reservation if package_type == 'car' else None,
                flight=reservation if package_type == 'flight' else None,
                bus=reservation if package_type == 'bus' else None,
                yacht=reservation if package_type == 'yacht' else None,
                theme_park=reservation if package_type == 'theme-park' else None,
                top_attraction=reservation if package_type == 'top-attraction' else None,
                desert_safari=reservation if package_type == 'desert-safari' else None,
                water_park=reservation if package_type == 'water-park' else None,
                water_activity=reservation if package_type == 'water-activity' else None,
                adventure_tour=reservation if package_type == 'adventure-tour' else None,
                combo_tour=reservation if package_type == 'combo-tour' else None,
                dubai_activity=reservation if package_type == 'dubai-activity' else None,
                payment_amount = amount,
                order_id = p_order_id
            )
            

            fin = Template(html).safe_substitute(mid=p_merchant_id, encReq=encryption, xscode=accessCode)
            soup = BeautifulSoup(fin, 'html.parser')

            # Find the iframe element with the ID 'paymentFrame'
            iframe = soup.find('iframe', {'id': 'paymentFrame'})

            if iframe:
                src = iframe['src']
                parsed_url = urlparse(str(src))
                query_params = parse_qs(parsed_url.query)

                merchant_id = query_params.get('merchant_id', [None])[0]
                encRequest = query_params.get('encRequest', [None])[0]
                access_code = query_params.get('access_code', [None])[0]
            return Response({'mid':merchant_id,'encReq':encRequest,"xscode":access_code,'url':str(src)},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        


@csrf_exempt
def PaymentConfirmationView(request):
    if request.method =='POST':
        try:
            encrypted_response = request.POST.get('encResp')
            plain_text = res(encrypted_response)
            soup = BeautifulSoup(plain_text, 'html.parser')

            order_status_element = soup.find('td', text='order_status')
            order_id_element = soup.find('td', text='order_id')

            if order_status_element and order_id_element:
                order_status = order_status_element.find_next('td').get_text().strip()
                order_id = order_id_element.find_next('td').get_text().strip()
            else:
                return redirect(settings.FRONTEND_URL+ '/payment/failed')

            
            
            booking = Booking.objects.get(order_id=order_id)
            if booking.status=='confirmed':
                return redirect(settings.FRONTEND_URL+ '/payment/success')
            if order_status=='Success':            
                booking.status = 'confirmed'
                booking.payment_status = 'paid'
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
                elif booking.yacht:
                    package = YachtReservation.objects.get(id=booking.package.id)
                    package.status = 'confirmed'
                    email = package.contact_email
                    phone = package.contact_phone
                    start_date = None
                    end_date = None
                    people = package.passenger
                    from_city = None
                    to_city = None
                    package.save()
                elif booking.theme_park:
                    package = ThemeParkReservation.objects.get(id=booking.package.id)
                    package.status = 'confirmed'
                    email = package.contact_email
                    phone = package.contact_phone
                    start_date = None
                    end_date = None
                    people = package.admission_count
                    from_city = None
                    to_city = None
                    package.save()
                elif booking.top_attraction:
                    package = TopAttractionReservation.objects.get(id=booking.package.id)
                    package.status = 'confirmed'
                    email = package.contact_email
                    phone = package.contact_phone
                    start_date = None
                    end_date = None
                    people = package.ticket_count
                    from_city = None
                    to_city = None
                    package.save()
                elif booking.desert_safari:
                    package = DesertSafariReservation.objects.get(id=booking.package.id)
                    package.status = 'confirmed'
                    email = package.contact_email
                    phone = package.contact_phone
                    start_date = None
                    end_date = None
                    people = package.participant_count
                    from_city = None
                    to_city = None
                    package.save()
                elif booking.water_park:
                    package = WaterParkReservation.objects.get(id=booking.package.id)
                    package.status = 'confirmed'
                    email = package.contact_email
                    phone = package.contact_phone
                    start_date = None
                    end_date = None
                    people = package.admission_count
                    from_city = None
                    to_city = None
                    package.save()
                elif booking.water_activity:
                    package = WaterActivityReservation.objects.get(id=booking.package.id)
                    package.status = 'confirmed'
                    email = package.contact_email
                    phone = package.contact_phone
                    start_date = None
                    end_date = None
                    people = package.participant_count
                    from_city = None
                    to_city = None
                    package.save()
                elif booking.adventure_tour:
                    package = AdventureTourReservation.objects.get(id=booking.package.id)
                    package.status = 'confirmed'
                    email = package.contact_email
                    phone = package.contact_phone
                    start_date = None
                    end_date = None
                    people = package.participant_count
                    from_city = None
                    to_city = None
                    package.save()
                elif booking.combo_tour:
                    package = ComboTourReservation.objects.get(id=booking.package.id)
                    package.status = 'confirmed'
                    email = package.contact_email
                    phone = package.contact_phone
                    start_date = None
                    end_date = None
                    people = package.participant_count
                    from_city = None
                    to_city = None
                    package.save()
                elif booking.dubai_activity:
                    package = DubaiActivityReservation.objects.get(id=booking.package.id)
                    package.status = 'confirmed'
                    email = package.contact_email
                    phone = package.contact_phone
                    start_date = None
                    end_date = None
                    people = package.participant_count
                    from_city = None
                    to_city = None
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
                    "start_date": datetime.strptime(str(start_date), "%Y-%m-%d").strftime("%d %B %Y") if start_date else '',
                    "end_date": datetime.strptime(str(end_date), "%Y-%m-%d").strftime("%d %B %Y") if end_date else ''
                }
                email_sent = send_booking_confirmation_email(context)
                pdf_content = save_pdf(pdf_params)
                booking.pdf.save(f'{uuid.uuid4()}.pdf',ContentFile(pdf_content))
                return redirect(settings.FRONTEND_URL+ '/payment/success')
            
            else:
                booking.status = 'failed'
                booking.payment_status = 'failed'
                booking.save()
                return redirect(settings.FRONTEND_URL+ '/payment/failed')
        except Exception as e:
            print(e)
            return redirect(settings.FRONTEND_URL+ '/payment/failed')
    

class BookingCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        try:
            booking = Booking.objects.filter(pk=pk,user=request.user).first()
            if booking.status == 'cancelled':
                return Response({'message': 'Booking is already cancelled'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                refund_amount = int(booking.payment_amount * 100)

                refund = RefundRequest.objects.create(
                    user = booking.user,
                    hotel=booking.hotel or None,
                    car = booking.car or None,
                    flight = booking.flight or None,
                    bus = booking.bus or None,
                    package = booking.package or None,
                    theme_park = booking.theme_park or None,
                    top_attraction = booking.top_attraction or None,
                    desert_safari = booking.desert_safari or None,
                    water_park = booking.water_park or None,
                    water_activity = booking.water_activity or None,
                    adventure_tour = booking.adventure_tour or None,
                    combo_tour = booking.combo_tour or None,
                    dubai_activity = booking.dubai_activity or None,
                    order_id = booking.order_id,
                    refund_amount = refund_amount
                )
                
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
                elif booking.yacht:
                    package = YachtReservation.objects.get(id=booking.package.id)
                    package.status = 'cancelled'
                    email = package.contact_email
                    package.save()
                elif booking.theme_park:
                    package = ThemeParkReservation.objects.get(id=booking.package.id)
                    package.status = 'cancelled'
                    email = package.contact_email
                    package.save()
                elif booking.top_attraction:
                    package = TopAttractionReservation.objects.get(id=booking.package.id)
                    package.status = 'cancelled'
                    email = package.contact_email
                    package.save()
                elif booking.desert_safari:
                    package = DesertSafariReservation.objects.get(id=booking.package.id)
                    package.status = 'cancelled'
                    email = package.contact_email
                    package.save()
                elif booking.water_park:
                    package = WaterParkReservation.objects.get(id=booking.package.id)
                    package.status = 'cancelled'
                    email = package.contact_email
                    package.save()
                elif booking.water_activity:
                    package = WaterActivityReservation.objects.get(id=booking.package.id)
                    package.status = 'cancelled'
                    email = package.contact_email
                    package.save()
                elif booking.adventure_tour:
                    package = AdventureTourReservation.objects.get(id=booking.package.id)
                    package.status = 'cancelled'
                    email = package.contact_email
                    package.save()
                elif booking.combo_tour:
                    package = ComboTourReservation.objects.get(id=booking.package.id)
                    package.status = 'cancelled'
                    email = package.contact_email
                    package.save()
                elif booking.dubai_activity:
                    package = DubaiActivityReservation.objects.get(id=booking.package.id)
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
    

class CustomerReviewView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,model,object_id):
        data = {**request.data,'user':request.user.id}
        if model == 'hotel':
            obj = get_object_or_404(Hotel, id=object_id)
            data = {**data,'hotel':object_id}
            serializer = HotelCustomerReviewSerializer(data=data)
        elif model == 'car':
            obj = get_object_or_404(Car, id=object_id)
            data = {**data,'car':object_id}
            serializer = CarCustomerReviewSerializer(data=data)
        elif model == 'flight':
            obj = get_object_or_404(Flight, id=object_id)
            data = {**data,'flight':object_id}
            serializer = FlightCustomerReviewSerializer(data=data)
        elif model == 'package':
            obj = get_object_or_404(Package, id=object_id)
            data = {**data,'package':object_id}
            serializer = PackageCustomerReviewSerializer(data=data)
        elif model == 'themepark':
            obj = get_object_or_404(ThemePark, id=object_id)
            data = {**data,'themepark':object_id}
            serializer = ThemeParkCustomerReviewSerializer(data=data)
        elif model == 'topattraction':
            obj = get_object_or_404(TopAttraction, id=object_id)
            data = {**data,'topattraction':object_id}
            serializer = TopAttractionCustomerReviewSerializer(data=data)
        elif model == 'desertsafari':
            obj = get_object_or_404(DesertSafari, id=object_id)
            data = {**data,'desertsafari':object_id}
            serializer = DesertSafariCustomerReviewSerializer(data=data)
        elif model == 'waterpark':
            obj = get_object_or_404(WaterPark, id=object_id)
            data = {**data,'waterpark':object_id}
            serializer = WaterParkCustomerReviewSerializer(data=data)
        elif model == 'wateractivity':
            obj = get_object_or_404(WaterActivity, id=object_id)
            data = {**data,'wateractivity':object_id}
            serializer = WaterActivityCustomerReviewSerializer(data=data)
        elif model == 'adventuretour':
            obj = get_object_or_404(AdventureTour, id=object_id)
            data = {**data,'adventuretour':object_id}
            serializer = AdventureTourCustomerReviewSerializer(data=data)
        elif model == 'combotour':
            obj = get_object_or_404(ComboTour, id=object_id)
            data = {**data,'combotour':object_id}
            serializer = ComboTourCustomerReviewSerializer(data=data)
        elif model == 'dubaiactivity':
            obj = get_object_or_404(DubaiActivity, id=object_id)
            data = {**data,'dubaiactivity':object_id}
            serializer = DubaiActivityCustomerReviewSerializer(data=data)
        elif model == 'yacht':
            obj = get_object_or_404(Yacht, id=object_id)
            data = {**data,'yacht':object_id}
            serializer = YachtCustomerReviewSerializer(data=data)

        if serializer.is_valid():
            review = serializer.save()
            review.yacht = obj
            review.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BannerListCreateView(generics.ListCreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

class SelfDriveRentalList(generics.ListCreateAPIView):
    queryset = SelfDriveRental.objects.all()
    serializer_class = SelfDriveRentalSerializer