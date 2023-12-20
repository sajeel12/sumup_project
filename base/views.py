from django.shortcuts import render

# from django.contrib.auth.models import User
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import check_password
import json
from openpyxl import Workbook
# from .forms import SignUpForm

import pycountry


@login_required(login_url="loginto")
def dashboard(request):
    access_token = request.session.get("sumup_access_token")
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
    return render(request, "base/dashboard.html")


def loginto(request):
    print("in loginto")
    page = "login"
    msg = ""
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            print(user, "<-- user")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("dashboard")
                else:
                    msg = "Account Pending for Approval"
            else:
                msg = "Account not approved"
        except:
            msg = "user not Exists "
    context = {"page": page, "msg": msg}
    return render(request, "base/login_signup.html", context)


def signupUser(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    page = "signup"
    msg = ""

    countries = list(pycountry.countries)

    if request.method == "POST":
        name = request.POST.get("name")
        # username = request.POST.get("username")
        email = request.POST.get("email")
        telephone = request.POST.get("telephone")
        address = request.POST.get("address")
        organisation_name = request.POST.get("organisation_name")
        country = request.POST.get("country")
        password = request.POST.get("password")
        confirmPassword = request.POST.get("confirmPassword")

        print(
            name,
            email,
            password,
            confirmPassword,
            country,
            telephone,
            address,
            organisation_name,
        )
        if (
            name
            and email
            and password
            and confirmPassword
            and country
            and telephone
            and address
            and organisation_name
        ):
            if password == confirmPassword:
                if User.objects.filter(email=email).exists():
                    msg = "Email already exists"
                else:
                    user = User(
                        # username=username,
                        email=email,
                        # password=password,
                        name=name,
                        telephone=telephone,
                        address=address,
                        organisation_name=organisation_name,
                        country_for_tax_purpose=country,
                    )
                    user.set_password(password)
                    user.is_active = False
                    user.save()
                    msg = "User Created Successfully"

                    return redirect("loginto")
            else:
                msg = "password not matched"
        # Redirect to your login page
    # else:
    #     form = SignUpForm()

    context = {"page": page, "countries": countries, "msg": msg}
    return render(request, "base/login_signup.html", context)


def logoutUser(request):
    print("in logout")
    logout(request)
    print("logged out")
    return redirect("loginto")


# views.py
@login_required(login_url="loginto")
def sumup_login(request):
    print("in sumup login")
    # Redirect the user to SumUp for authorization
    print(settings.SUMUP_CLIENT_ID, "sclient id ")
    authorization_url = "https://api.sumup.com/authorize"
    params = {
        "client_id": settings.SUMUP_CLIENT_ID,
        "redirect_uri": settings.SUMUP_REDIRECT_URI,
        "response_type": "code",
        "scope": "transactions.history user.profile user.profile_readonly",
        "state": "testing",  # Generate a unique state string for security
    }
    redirect_url = f'{authorization_url}?{"&".join(f"{key}={value}" for key, value in params.items())}'
    print(redirect_url)

    return redirect(redirect_url)


@login_required(login_url="loginto")
def sumup_callback(request):

    if not request.user.is_authenticated and request.user.is_active :
        return redirect("loginto")

    print("in sumup callback")

    # Handle the callback from SumUp after user authorization
    code = request.GET.get("code")

    # Exchange the authorization code for an access token
    token_url = "https://api.sumup.com/token"
    data = {
        "client_id": settings.SUMUP_CLIENT_ID,
        "client_secret": settings.SUMUP_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.SUMUP_REDIRECT_URI
        # "expires_in": 31536000
    }

    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()  # Raise an error for bad responses
        token_data = response.json()
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
    except requests.RequestException as e:
        return JsonResponse(
            {"error": f"Error exchanging code for token: {e}"}, status=500
        )


    print(access_token, "<-- access token")
    print(token_data.get("refresh_token"), "<-- access token")

    # Save the access token in the databases
    user  = User.objects.get(id=request.user.id)
    user.sumup_access_token = access_token
    user.sumup_refresh_token = refresh_token
    user.save()

    # Use the access token to get user information
    user_info_url = "https://api.sumup.com/v0.1/me"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info_response.raise_for_status()
        user_info = user_info_response.json()
    except requests.RequestException as e:
        return JsonResponse(
            {"error": f"Error fetching user information: {e}"}, status=500
        )

    print(user_info, "<-- user info")


    email = (
        user_info.get("merchant_profile", {}).get("doing_business_as", {}).get("email")
    )

    print(email)

    # Authenticate or create the user in your Django application
    if email:
        return redirect("dashboard")
    else:
        return JsonResponse({"error": "User authentication failed"}, status=400)

# @login_required(login_url="loginto")
def refresh_access_token(refresh_token,user):
    print('                    in refresh function')

    token_url = "https://api.sumup.com/token"

    data = {
        'client_id': settings.SUMUP_CLIENT_ID,
        'client_secret':  settings.SUMUP_CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }

    try:
        print('                    in refresh try')

        response = requests.post(token_url, data=data)
        print('                    in after response function')

        response.raise_for_status()  # Raise an error for bad responses
        token_data = response.json()
        new_access_token = token_data.get("access_token")
        new_refresh_token = token_data.get("refresh_token")

        # user  = User.objects.get(id=request.user.id)
        user.sumup_access_token = new_access_token
        user.sumup_refresh_token = new_refresh_token
        user.save()
        print('                    user saved refresh success')
    except requests.RequestException as e:
        return JsonResponse(
            {"error": f"Error exchanging code for token: {e}"}, status=500
        )

    
    


def reports(request):
    return render(request, "base/reports.html")

@login_required(login_url="loginto")
def user_management(request):
    if request.user.is_admin or request.user.is_superuser:
        users = User.objects.all()
        context = {"users": users}
        return render(request, "base/user_management.html", context)
    else:
        return redirect("dashboard")


# ===================== Api Fucnitons  S ======================================================================

@login_required(login_url="loginto")
def approve_user(request):
    if request.user.is_admin or request.user.is_superuser:
        user_data = json.loads(request.body)
        if user_data["active"]:
            user = User.objects.get(id=user_data["id"])
            user.is_active = True
            user.save()
            return JsonResponse({"data": "User Approved"})

    return redirect("user_management")

@login_required(login_url="loginto")
def get_users(request):
    print(request.user.is_admin, "<-- is admin")
    if request.user.is_admin or request.user.is_superuser:
        users = User.objects.filter(is_active=False)
        users = list(users.values())
        return JsonResponse({"users": users})
    else:
        return JsonResponse({"data": "Not Authorized"})


@login_required(login_url="loginto")
def get_total_transactions(request):
    access_token = request.user.sumup_access_token
    print(access_token, "<-- access token in get total transactionss ")
    if access_token:
        try:
            transactionss_info_url = (
                "https://api.sumup.com/v0.1/me/transactions/history/"
            )
            headers = {"Authorization": f"Bearer {access_token}"}
            params = {
                "limit": 5000,
            }
            transactions_info_response = requests.get(
                transactionss_info_url, headers=headers, params=params
            )
            response = transactions_info_response.json()
            # json_response = json.loads(response)
            # print(json_response, "<-- transactions  response")
            # print(response['error_message'], 'error message')
            try:
                if response['error_message']:
                    new_access_token = refresh_access_token(request.user.sumup_refresh_token,request.user)
                    headers = {"Authorization": f"Bearer {new_access_token}"}
                    transactions_info_response = requests.get(
                        transactionss_info_url, headers=headers, params=params
                    )
                    response = transactions_info_response.json()
            
            except:
                pass
            print(response, "<-- transactions  response")
            return JsonResponse({"data": response})
        except:
            print("error in get total transactions")
            return JsonResponse({"error": "error in get total transactions"})




# ===================== Api Fucnitons E =======================================================================

@login_required(login_url="loginto")
def download_excel(request):
    # Sample data (replace this with your actual data)
    data = get_total_transactions(request)
    data = json.loads(data.content)
    print(data['data']['items'][0])
    data =  data['data']['items']
 
 

    # Create a new workbook and add a worksheet
    wb = Workbook()
    ws = wb.active

    # Write header
    header = list(data[0].keys())
    print(header, '<-- header')
    ws.append(header)
    # for row in header:
        # ws.append(row)
    # Write data
    for row_data in data:
        try:
            ws.append([row_data[key] for key in header])
        except:
            pass

    # Create a response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=transaction_data.xlsx'

    # Save the workbook to the response
    wb.save(response)

    return response
