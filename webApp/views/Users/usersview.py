from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
import os
from webApp.models import *
from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpResponse 
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests as googlereq
import jwt
import requests


def  RegisterAdmin(request):
    if  request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            User.objects.create_user(username=username,password=password)

            return redirect(request.META.get('HTTP_REFERER')) 
    else:
        messages.warning(request, 'Only super admin can create admin user !')
        return redirect(request.META.get('HTTP_REFERER'))
    

# def  Adminpanel(request):
#     if  request.user.is_authenticated and request.user.is_staff:
#         return render(request,)

from requests_oauthlib import OAuth2Session
from webApp.views.Others.geocode_address import *

LINKEDIN_API_BASE_URL = 'https://api.linkedin.com/v2/'
LINKEDIN_USER_INFO_URL = 'https://api.linkedin.com/v2/me'
# Define your LinkedIn credentials and endpoints
client_id = '774yjmsuovwh04'
client_secret = 'UJJwU1s84cVQVXxv'
redirect_uri = 'http://localhost:8000/lnkd_logi'
authorization_base_url = 'https://www.linkedin.com/oauth/v2/authorization'
token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
# Create an OAuth2 session
linkedin = OAuth2Session(client_id, redirect_uri=redirect_uri, scope='openid profile email w_member_social')

def sign_in(request):  
    # get_lat_long_nominatim()
    # lat_long_nearest_kitchen() 
    #address = "1292 Mt Mills Rd, Tuscumbia, AL 35674, United States"
    #address = "9KM Pir Sohawa Road, Islamabad, Islamabad Capital Territory"
    #address = "100 Southside Square, Huntsville, AL 35801, United States"
    # address = "9KM Pir Sohawa Road, Islamabad, Islamabad Capital Territory"
    #address =  u'394 Street 15, Chaklala Scheme 3 Chaklala Housing Scheme 3, Rawalpindi, Punjab 46000, Pakistan'
    #address = u'Plot 52, Commercial Area Rd, Chaklala Housing Scheme 3, Rawalpindi, 46000, Pakistan'
    # address = "390 Street 15, Chaklala Scheme 3 Chaklala Housing Scheme 3, Rawalpindi, Punjab 46000, Pakistan"
    # print("pelias appp",geocode_earth_api_for_address(address))
    # print("geocdo appp",geocodio_api_for_address(address))
    # lat, long = ola_map_for_address(address)
    # print("lat opncg,long opncg",lat,long)
    # lat, long = OpenCage_for_address(address)
    # print("lat opncg,long opncg",lat,long)
    # get_lat_long_nominatim()
    if 'user_data' in  request.session:
        print("g")
        return redirect('order_item_listing_page')
    if 'soc_loged' in  request.session:
        # del request.session['soc_loged']
        print("f")  
        return redirect('order_item_listing_page')
    if 'lnkd_loged' in  request.session:
        print("l")
        return redirect('order_item_listing_page')
        return render(request, 'Users/client_sign_in.html')

    

    

    # Step 1: User Authorization
    authorization_url, state = linkedin.authorization_url(authorization_base_url)
    print(f'Please go to this URL and authorize access: {authorization_url}')

   
    

    return render(request, 'Users/client_sign_in.html',{'linkdnur':authorization_url})



def lnkd_log_redirect(request): 
    # print("lnkd_log_redirect",request.GET.get('code'))


    # Exchange the authorization code for an access token
    token_response = requests.post(
        token_url,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={
            'grant_type': 'authorization_code',
            'code': request.GET.get('code'),
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret
        }
    )
    token_response.raise_for_status()
    token_data = token_response.json()
    access_token = token_data['access_token']
    profile_response = requests.get("https://api.linkedin.com/v2/userinfo", headers={'Authorization': f'Bearer {access_token}'})

    # Fetch the user's profile
    # profile_response = requests.get(
    #     LINKEDIN_USER_INFO_URL,
    #     headers={'Authorization': f'Bearer {access_token}'}
    # )
    # # profile_response.raise_for_status()
    # profile_data = profile_response.json()
   
    # token = linkedin.authorize_access_token()
    # user_info = linkedin.parse_id_token(token)

    # token = linkedin.fetch_token(
    #     token_url,
    #     client_secret=client_secret,
    #     authorization_response=request.url
    # )


    # # Fetch user profile information
    # response = linkedin.get(LINKEDIN_API_BASE_URL + 'me?projection=(id,firstName,lastName)')
    # user_info = response.json()

    # linkedinhui = OAuth2Session(client_id, redirect_uri=redirect_uri)
    # token = linkedinhui.fetch_token(
    #     token_url,
    #     client_secret=client_secret,
    #     authorization_response=request.url
    # )

    # linkedincdf = OAuth2Session(client_id, token=access_token)
    # profile_response = linkedincdf.get(f'{LINKEDIN_API_BASE_URL}/me')
    profile_response = profile_response.json()

   
    print('Profile Info:', profile_response)


    

    # # Step 2: Get the authorization verifier code from the callback URL
    # redirect_response = input('Paste the full redirect URL here: ')
    # oauth.fetch_token(token_url, authorization_response=redirect_response, client_secret=client_secret)



    #  # Fetch user profile information
    # response = linkedin.get(LINKEDIN_API_BASE_URL + 'me?projection=(id,firstName,lastName)')
    # user_info = response.json()

    # token = oauth2_session.fetch_token(
    #     token_url,
    #     client_secret=client_secret,
    #     authorization_response=request.get_full_path()
    # )

    # Step 3: Fetch the user's profile information
    # response = oauth.get(USER_INFO_URL)
    # profile_info = response.json()
    # print('Profile Info:', profile_info)

    request.session['lnkd_loged'] = True

    request.session['lnkd_name'] = profile_response['name']

    request.session['lnkd_email'] = profile_response['email']

    request.session['lnkd_profi'] = profile_response['picture']

    return redirect('sign_in')


@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    print("floli",request.POST)
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, googlereq.Request(),  settings.GOOGLE_OAUTH_CLIENT_ID
        )
    except ValueError:
        return HttpResponse(status=403)

    # In a real app, I'd also save any new user here to the database. See below for a real example I wrote for Photon Designer.
    # You could also authenticate the user here using the details from Google (https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)
    request.session['user_data'] = user_data

    print("sogneee userdt",user_data)

    return redirect('sign_in')


@csrf_exempt
def socback_log_redirect(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    print("socback_log_redirect",request.POST)
    request.session['soc_loged'] = True 
    return redirect('sign_in')

def sign_out(request):
    # print("redeq",request.session)
    if 'user_data' in  request.session:
        del request.session['user_data']
    if 'soc_loged' in  request.session:
        del request.session['soc_loged']
        logout(request)
    if 'lnkd_loged' in  request.session:
        del request.session['lnkd_loged'] 
    return redirect('sign_in')

    

#Google auto address filler

def  Auto_fill_address_form(request):
    if request.method == 'POST':
        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        country = request.POST.get('country')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
 

        return HttpResponse('Address saved successfully!')

    return render(request, 'Users/auto_fill_address_form.html', {
        'GOOGLE_API_KEY': 'your_api_key_here'
    })