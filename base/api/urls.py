# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='user-login'),
    path('donors/', views.create_donor, name='create-donor'),
    path('verify/', views.verify_user, name='verify-user'),

]
