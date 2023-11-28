from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render





@login_required(login_url='loginto')
def dashboard(request):
    access_token = request.session.get('sumup_access_token')
    # def get_checkouts():
    #     pass

    # if access_token :
    #     try:
    #         user_info_url = 'https://api.sumup.com/v0.1/me'
    #         headers = {'Authorization': f'Bearer {access_token}'}
    #         user_info_response = requests.get(user_info_url, headers=headers)
    #         user_info = user_info_response.json()
    #         username = user_info['account']['username']

    #         context = {'username': username }

    #         return render(request, 'base/dashboard.html', context)
    #     except:
    #         pass
    # else:
    return render(request, 'base/dashboard.html')



def loginto(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    page = 'login'

    context = {
        'page': page
    }
    return render(request, 'base/login.html', context)


def logoutUser(request):
    print('in logout')
    logout(request)
    print('logged out')
    return redirect('loginto')


# views.py
def sumup_login(request):
    print('in sumup login')
    # Redirect the user to SumUp for authorization
    print(settings.SUMUP_CLIENT_ID, 'sclient id ')
    authorization_url = 'https://api.sumup.com/authorize'
    params = {
        'client_id': settings.SUMUP_CLIENT_ID,
        'redirect_uri': settings.SUMUP_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'transactions.history user.profile user.profile_readonly',
        'state': 'testing',  # Generate a unique state string for security
    }
    redirect_url = f'{authorization_url}?{"&".join(f"{key}={value}" for key, value in params.items())}'
    print(redirect_url)
    
    return redirect(redirect_url)

def sumup_callback(request):
    print('in sumup callback')
    # Handle the callback from SumUp after user authorization
    code = request.GET.get('code')

    # Exchange the authorization code for an access token
    token_url = 'https://api.sumup.com/token'
    data = {
        'client_id': settings.SUMUP_CLIENT_ID,
        'client_secret': settings.SUMUP_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': settings.SUMUP_REDIRECT_URI,
    }
    response = requests.post(token_url, data=data)
    print(response)
    token_data = response.json()
    access_token = token_data.get('access_token')

    # Assuming you have obtained the SumUp access token and stored it in the variable 'access_token'
    request.session['sumup_access_token'] = access_token
    request.session.set_expiry(3600)  # Set session expiration time (in seconds), adjust as needed


    print(access_token, '<-- access token')

    # Use the access token to make a request to get user information
    user_info_url = 'https://api.sumup.com/v0.1/me'
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()
    print(user_info, '<-- user info')


    username = user_info['account']['username']
    email = user_info['merchant_profile']['doing_business_as']['email']

    print(username, ' + ',email)

    # Authenticate or create the user in your Django application
    user_db = None
    if username is not None:
        try:
            print(116)
            user_db = User.objects.filter(username=username).first()
            print(119)
        except:
            user_db = None
            print(122)

        if user_db is None:
            print('in  userdb ')
            user_db = User.objects.create_user(username, email)

        print('trying to login')
        # authenticated_user = authenticate(request, username=username, email=email)
        login(request,  authenticated_user)
        # return HttpResponse(f'Logged in as {username}')
        print('redi to dashboard')
        return redirect('dashboard')
    else:
        print('user is none')
        return HttpResponse('User authentication failed')


# ===================== Api Fucnitons  S ======================================================================

def get_total_checkouts(request):
    access_token = request.session.get('sumup_access_token')
    print(access_token, '<-- access token in get total checkouts ')
    if access_token :
        try:
            checkouts_info_url = 'https://api.sumup.com/v0.1/checkouts'
            headers = {'Authorization': f'Bearer {access_token}'}
            checkout_info_response = requests.get(checkouts_info_url, headers=headers)
            checkout = checkout_info_response.json()
            

            return JsonResponse({ "data": checkout})
        except:
            pass

def get_total_transactions(request):
    access_token = request.session.get('sumup_access_token')
    print(access_token, '<-- access token in get total transactionss ')
    if access_token :
        try:
            transactionss_info_url = 'https://api.sumup.com/v0.1/me/transactions/history'
            headers = {'Authorization': f'Bearer {access_token}'}
            transactions_info_response = requests.get(transactionss_info_url, headers=headers)
            transactions = transactions_info_response.json()
            return JsonResponse({ "data": transactions})
        except:
            pass

def get_total_financialpayouts(request):
    access_token = request.session.get('sumup_access_token')
    print(access_token, '<-- access token in get total transactionss ')
    if access_token :
        try:
            url = 'https://api.sumup.com/v0.1/me/financials/payouts'
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(url, headers=headers)
            response = response.json()
            return JsonResponse({ "data": response})
        except:
            pass


# ===================== Api Fucnitons E =======================================================================
