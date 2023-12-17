# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='user-login'),
    path('donors/', views.create_donor, name='create-donor'),
    # path('get/', views.getRoutes, name='user-login'),
    # path('check-email/', views.check_email_exists, name='check_email_exists'),

    # getRoutes
]
