from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserLoginSerializer, DonorSerializer
from django.contrib.auth import authenticate
from base.models import User
import requests
from django.shortcuts import get_object_or_404


@api_view(["POST"])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]

    # Check if the user already has a token, create one if not
    Token.objects.filter(user=user).delete()
    token, created = Token.objects.get_or_create(user=user)

    return Response({"token": token.key}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_donor(request):
    if request.method == "POST":
        data = request.data
        serializer = DonorSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
def verify_user(request):
    merchant_code = request.data.get("merchant_code")
    # access_token = request.data.get("access_token")

    # user = User.objects.get(merchant_code=merchant_code)

    # print(access_token, " <--------------------- access_token  \n \n \n  ")
    # print(user.sumup_access_token, " <--------------------- access_token  \n \n \n  ")



    # Request to Sumup API
    # sumup_api_url = "https://api.sumup.com/v0.1/me"
    # headers = {"Authorization": f"Bearer {access_token}"}

    # try:
    #     response = requests.get(sumup_api_url, headers=headers)
    #     response.raise_for_status()
    #     user_data = response.json()
    # except requests.exceptions.RequestException as e:
    #     return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # # Verify merchant_code (assuming it's present in user_data)
    # print(user_data, " <--------------------- user_data  \n \n \n  " )
    # merchant_code_res = user_data['merchant_profile']['merchant_code']


    # print(merchant_code_res, " <--------------------- merchant_code_res  \n \n \n  " )

    # Assuming 'merchant_code' is a field in your User model
    try:
        
        user = User.objects.get(merchant_code=merchant_code)
        # if not user.merchant_code == merchant_code_res:
        #     return Response({"status": True}, status=status.HTTP_200_OK)

        # Delete existing tokens for the user
        Token.objects.filter(user=user).delete()

        # Generate a new token for the user
        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key, "status": True}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found", "status": False}, status=status.HTTP_404_NOT_FOUND)
