# myapp/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from base.models import User

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])

        if not user:
            raise serializers.ValidationError('Invalid email or password')

        data['user'] = user 
        return data
    
# class UserProfileSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         user = authenticate(email=data['email'], password=data['password'])

#         if not user:
#             raise serializers.ValidationError('Invalid email or password')

#         data['user'] = user 
#         return data