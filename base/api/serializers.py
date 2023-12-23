# myapp/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from base.models import User, Donor

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])

        if not user:
            raise serializers.ValidationError('Invalid email or password')

        data['user'] = user 
        return data
    


class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = '__all__'


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'