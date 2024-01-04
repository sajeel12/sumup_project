# myapp/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from base.models import User, Donor


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        data["user"] = user
        return data


class DonorSerializer(serializers.ModelSerializer):
    required_fields = [
        "full_name",
        "address",
        "postcode",
        "transaction_code",
        "amount_in_pounds",
        "timestamp",
    ]  # Add your required fields here

    class Meta:
        model = Donor
        fields = "__all__"

    def validate(self, data):
        for field in self.required_fields:
            if field not in data or data[field] is None:
                raise serializers.ValidationError(f"{field} is required")
        return data


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
