# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='user-login'),
    path('get/', views.getRoutes, name='user-login'),

    # getRoutes
]
