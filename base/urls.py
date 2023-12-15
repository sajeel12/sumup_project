from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('loginto/', views.loginto, name='loginto'),
    path('logout/', views.logoutUser, name='logout'),
    path('signup/', views.signupUser, name='signup'),

    path('sumup/login/', views.sumup_login, name='sumup_login'),
    path('sumup/callback/', views.sumup_callback, name='sumup_callback'),

    path('sumup/transactions/', views.get_total_transactions, name='sumup_transactions'),

    

    path('reports/', views.reports, name='reports'),
    path('usermanagement/', views.user_management, name='user_management'),


    # apis
    path('get-users/', views.get_users, name='get_users'),
    path('approve-user/', views.approve_user, name='approve_users'),

    # path('download-excel/<str:start_date>/<str:end_date>/', views.download_excel, name='download_excel'),
    path('download-excel/', views.download_excel, name='download_excel'),


]