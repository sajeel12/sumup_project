from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard , name='dashboard'),
    path('loginto/', views.loginto , name='loginto'),
    path('logout/', views.logoutUser , name='logout'),
    path('sumup/login/', views.sumup_login, name='sumup_login'),
    path('sumup/callback/', views.sumup_callback, name='sumup_callback'),

    path('sumup/checkouts/', views.get_total_checkouts, name='sumup_checkouts'),
    path('sumup/transactions/', views.get_total_transactions, name='sumup_transactions'),
    path('sumup/financialpayouts/', views.get_total_financialpayouts, name='finanacialpayouts'),

]