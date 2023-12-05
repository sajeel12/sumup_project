# your_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

#     class Meta:
#         model = User  # Use your custom user model
#         fields = [ 'email', 'phone_no' ,'password1', 'password2']
