from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','name','phone','gender','merital_status','birthday','address','pin','state','provider']


class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name','phone','gender','merital_status','birthday','address','pin','state')