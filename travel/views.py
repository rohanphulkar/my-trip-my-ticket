from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework import status,filters, generics
from rest_framework.response import Response
from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TourPriceFilter

class ToursView(generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filter_class = TourPriceFilter
    search_fields = ['location']
    
    

class TourDetailView(APIView):
    def get(self,request,id):
        try:
            tour = Tour.object.get(id=id)
            serializer = TourSerializer(tour,many=False)
            return Response({'message':'tour details recieved successfully','tour':serializers.data})
        except Exception as e:
            return Response({'message':'tour not found'},status=status.HTTP_404_NOT_FOUND)

class HotelView(APIView):
    def get(self,request):
        hotels = Hotel.objects.all()
        serializers = HotelSerializer(hotels,many=True)
        return Response({'message':'hotels recieved successfully','hotels':serializers.data},status=status.HTTP_200_OK)


class HotelDetailView(APIView):
    def get(self,request,id):
        try:
            hotel = Hotel.object.get(id=id)
            serializer = HotelSerializer(hotel,many=False)
            return Response({'message':'hotel details recieved successfully','hotel':serializers.data})
        except Exception as e:
            return Response({'message':'hotel not found'},status=status.HTTP_404_NOT_FOUND)
        
class CarView(APIView):
    def get(self,request):
        cars = Car.objects.all()
        serializers = CarSerializer(cars,many=True)
        return Response({'message':'cars recieved successfully','cars':serializers.data},status=status.HTTP_200_OK)


class CarDetailView(APIView):
    def get(self,request,id):
        try:
            car = Car.object.get(id=id)
            serializer = CarSerializer(car,many=False)
            return Response({'message':'car details recieved successfully','car':serializers.data})
        except Exception as e:
            return Response({'message':'car not found'},status=status.HTTP_404_NOT_FOUND)


class AdImageView(APIView):
    def get(self, request):
            images = AdImage.objects.filter(user=request.user)
            serializer = AdImageSerializer(images, many=True)
            return Response(serializer.data)

class UserItineraryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        if pk:
            itinerary = UserItinerary.objects.get(pk=pk)
            serializer = UserItinerarySerializer(itinerary)
            return Response(serializer.data)
        else:
            itineraries = UserItinerary.objects.filter(user=request.user)
            serializer = UserItinerarySerializer(itineraries, many=True)
            return Response(serializer.data)


class BookingView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        if pk:
            bookings = Booking.objects.get(pk=pk)
            serializer = BookingSerializer(bookings)
            return Response(serializer.data)
        else:
            bookings = Booking.objects.filter(user=request.user)
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data)