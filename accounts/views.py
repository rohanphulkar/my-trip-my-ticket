from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.views import APIView
import uuid
from .helper import send_password_reset_email,send_otp
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .serializers import EditProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken
import random
import jwt

class LoginView(APIView):
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email)
        if not user:
            if not len(password) >=8:
                return Response({'error':'Password must have minimum 8 character'},status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create(email=email,provider='email')
            user.set_password(password)
            user.save()
            return Response({'message':'Account created successfully'},status=status.HTTP_200_OK)
        user = User.objects.get(email=email)
        if user.provider!='email':
            return Response({'error':'Please try login through phone number or google acccount.'},status=status.HTTP_401_UNAUTHORIZED)
        if not user.check_password(password):
            return Response({'error':'Invalid password'},status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken.for_user(user)
        return Response({'message':'login successfully','token':str(token.access_token),'email':user.email},status=status.HTTP_200_OK)

    

class SendOTPView(APIView):
    def post(self,request):
        phone = request.data.get('phone')
        otp = random.randint(100000,999999)
        try:
            user = User.objects.get(phone=phone)
            if user.provider!='phone':
                return Response({'error':'Please try login through email or google acccount.'},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            user = User.objects.create(phone=phone,provider='phone')
        user.otp = otp
        user.save()
        otp_sent = send_otp(phone,otp)
        if not otp_sent:
            return Response({'error':'failed to sent otp.'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'An otp has been sent to your mobile number'},status=status.HTTP_200_OK)
    
class VerifyOTPView(APIView):
    def post(self,request):
        otp = request.data.get('otp')
        try:
            user = User.objects.get(otp=otp)
        except Exception as e:
            return Response({'error':'otp is invalid'},status=status.HTTP_404_NOT_FOUND)
        token = RefreshToken.for_user(user)
        user.otp = ''
        user.save()
        return Response({'message':'login successfully','token':str(token.access_token),'email':user.email},status=status.HTTP_200_OK)

class GoogleLogin(APIView):
    def post(self, request):
        token = request.data.get('token')
        try:
            decoded_token = jwt.decode(token, options={"verify_signature": False})
    
            name = decoded_token['name']
            email = decoded_token['email']
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        try:    
            user = User.objects.get(email=email)
            if user.provider!='google':
                return Response({'error':'Please try login through email or phone number.'},status=status.HTTP_400_BAD_REQUEST)
        except:
            user = User.objects.create(email=email,name=name,provider='google')
        token = RefreshToken.for_user(user)
        return Response({'token': str(token.access_token),'email':user.email}, status=status.HTTP_200_OK)

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error':'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        token = str(uuid.uuid4())
        url = f"{settings.FRONTEND_URL}/reset/{token}"
        user.pwd_reset_token = token
        user.save()
        email_sent = send_password_reset_email(user.email,url)
        if not email_sent:
            return Response({'error':'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success':'An email has been sent to your email address'}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    def post(self, request,token):
        try:
            user = User.objects.get(pwd_reset_token=token)
        except User.DoesNotExist:
            return Response({'error':'Token is invalid or expired'}, status=status.HTTP_404_NOT_FOUND)
        
        password = request.data['password']
        password2 = request.data['password2']
        
        if password != password2:
            return Response({'error':'Passwords do not match'},status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(password)
        user.save()
        return Response({'success':'Your password has been changed'}, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = User.objects.get(email=request.user)
        current_password = request.data['current_password']
        new_password = request.data['new_password']
        confirm_password = request.data['confirm_password']

        if not user.check_password(current_password):
            return Response({'error':'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
        if new_password != confirm_password:
            return Response({'error':'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({'success':'Your password has been changed'}, status=status.HTTP_200_OK)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user,many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        serializer = EditProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckTokenValidityView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            return Response({'message': 'Token is valid.'})
        except InvalidToken:
            return Response({'message': 'Token is not valid.'}, status=status.HTTP_400_BAD_REQUEST)