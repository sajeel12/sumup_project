from django.db import models

# Create your models here.

# your_app/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Add your custom fields here
    name = models.CharField(max_length=100, null=True)
    # username = models.CharField(max_length=100, null=True, unique=True)
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    telephone = models.CharField(max_length=20, null=True)
    organisation_name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=255, null=True)
    country_for_tax_purpose = models.CharField(max_length=100, null=True)

    
    sumup_access_token = models.CharField(max_length=255, null=True, blank=True)
    sumup_refresh_token = models.CharField(max_length=255, null=True, blank=True)

    merchant_code = models.CharField(max_length=100, null=True, blank=True)
    
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    

    def __str__(self):
        return self.email


class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='devices')
    model = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    display_resolution = models.CharField(max_length=255)
    android_version = models.CharField(max_length=255)
    device_id = models.CharField(max_length=255, unique=True)
    device_type = models.CharField(max_length=255)
    country_location = models.CharField(max_length=255, null=True, blank=True)
    location_cordinates = models.CharField(max_length=255, blank=True, null=True)

    # Add any other fields related to the device as needed

    def __str__(self):
        return f"{self.user.email} - {self.merchant_code} - {self.model}"


class Donor(models.Model):
    title = models.CharField(max_length=255)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=10)
    phoneNumber = models.CharField(max_length=15)
    emailAddress = models.EmailField()
    transactionCode = models.CharField(max_length=255, null=True, blank=True)
    amountInPounds = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    merchantCode = models.CharField(max_length=255, null=True, blank=True)
    productInformation = models.TextField(null=True, blank=True)
    subscribe = models.BooleanField(default=False)


