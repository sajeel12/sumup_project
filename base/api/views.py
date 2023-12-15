# myapp/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserLoginSerializer
from django.contrib.auth import authenticate
from base.models import User

@api_view(['POST'])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',                     # decalring api routes
        'GET /api/rooms',                     # decalring api routes
        'GET /api/rooms/:id'
    ]
    return Response(routes)  

@api_view(['GET'])
def check_email_exists(request, email):
    try:
        user_profile = User.objects.get(email=email)
        serializer = User(user_profile)
        return Response({'exists': True})
    except User.DoesNotExist:
        return Response({'exists': False})
