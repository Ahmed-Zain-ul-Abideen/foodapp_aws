from geopy.geocoders import Nominatim
nom = Nominatim(user_agent="ktkasad414@gmail.com",timeout=4)
import requests
from webApp.models import *
from django.db.models import Q
import googlemaps
import requests
from django.db.models import Func,F
from opencage.geocoder import OpenCageGeocode

# olampclient = OlmapC(client_id="0009258b-48c8-4609-b187-d4adc2819f3c", client_secret="MNwv7CFgTYyNtWLvhb1AgLtiLiHJTMCd")
# olampclient = OlmapC(api_key="RWV0zkGGd4Eze8BB3TTCNPtMLX6YAqOJTPTct8Gb")
opcggeocoder = OpenCageGeocode("205347dac04e47b992a3a61613134f48")

class Sin(Func):
    function = 'SIN'

class Cos(Func):
    function = 'COS'

class Acos(Func):
    function = 'ACOS'

class Radians(Func):
    function = 'RADIANS'

def Geocodeaddress():
    return nom

def OpcgGeocodeaddress():
    return opcggeocoder


# def OlamapGeocodeaddress(): 
#     return  olampclient





PELIAS_ENDPOINT = 'https://api.pelias.io/v1/search'
PELIAS_API_KEY = 'ge-2c7905cdb1bbc5a9'


import json
import urllib.request 
import urllib.parse
GEOCODE_EARTH_URL = 'https://api.geocode.earth/v1/search'

def  geocode_earth_api_for_address(address):

    # Prepare the request parameters
    params = {
        'text': address,
        'api_key': PELIAS_API_KEY
    }
    query_string = urllib.parse.urlencode(params)
    url = f"{GEOCODE_EARTH_URL}?{query_string}"
    
    try:
        # Make the request
        with urllib.request.urlopen(url) as response:
            data = response.read()
            response_json = json.loads(data)
            
            features = response_json.get('features', [])
            
            if features:
                result = features[0]
                geometry = result.get('geometry', {})
                properties = result.get('properties', {})
                return {
                    'latitude': geometry.get('coordinates', [])[1],
                    'longitude': geometry.get('coordinates', [])[0],
                    'address': properties.get('label', 'No address available')
                }
            else:
                return None

    except urllib.error.URLError as e:
        raise Exception(f"Geocoding API Error: {str(e)}")

    # query = "https://api.geocode.earth/v1/search?" \
    #         "api_key="+PELIAS_API_KEY+"&"\
    #         "text=100 Southside Square, Huntsville, AL 35801, United States"

    # response = json.load(urllib.request.urlopen(query))

    # print(response) # print the entire response

    # print(response['features'][0]['properties']['name'])      # London
    # print(response['features'][0]['properties']['label'])     # London, England, United Kingdom
    # print(response['features'][0]['geometry']['coordinates']) # [ -0.099076, 51.509648 ]


    # return True


def pelias_api_for_address(address):
    params = {
        'text': address,
        'api_key': PELIAS_API_KEY  # Include this if required by your Pelias instance
    }
    response = requests.get(PELIAS_ENDPOINT, params=params)
    data = response.json()

    if response.status_code == 200:
        features = data.get('features', [])
        if features:
            # Extract the first result
            result = features[0]
            properties = result.get('properties', {})
            geometry = result.get('geometry', {})
            return {
                'latitude': geometry.get('coordinates', [])[1],
                'longitude': geometry.get('coordinates', [])[0],
                'address': properties.get('label', 'No address available')
            }
        else:
            return None
    else:
        raise Exception(f"Pelias API Error: {data.get('message', 'Unknown error')}") 

GEOCODIO_API_KEY = '52ceaca067ec5701c60150a116a66c6c667a6ea'

def geocodio_api_for_address(address):  
    url = 'https://api.geocod.io/v1.6/geocode'
    params = {
        'q': address,
        'api_key': GEOCODIO_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200 and 'results' in data:
        if data['results']:
            result = data['results'][0]
            return {
                'latitude': result['location']['lat'],
                'longitude': result['location']['lng']
            }
        else:
            return None
    else:
        raise Exception(f"Geocoding API Error: {data.get('error', 'Unknown error')}")

def ola_map_for_address(address):  
    olampamnom = OlamapGeocodeaddress()
    results = olampamnom.geocode(address)
    print("results olamap",results[0]['geometry']['location']['lat'],results[0]['geometry']['location']['lng'])
    return True,True
    # api_key = 'RWV0zkGGd4Eze8BB3TTCNPtMLX6YAqOJTPTct8Gb'  # Replace with your Ola Maps API key
    
    # # Ola Maps Geocoding API endpoint (replace with actual endpoint)
    # url = f'https://api.ola.maps.com/geocode?address={address}&key={api_key}'
    
    # # Make the request to the Ola Maps API
    # response = requests.get(url)
    # data = response.json()

    # # Extract latitude and longitude from the response
    # if 'results' in data and len(data['results']) > 0:
    #     location = data['results'][0]['geometry']['location']
    #     latitude = location['lat']
    #     longitude = location['lng']
    #     return latitude,longitude
    # else:
    #     return None,None


def  OpenCage_for_address(location):
    # Replace 'YOUR_API_KEY' with your actual OpenCage API key
    api_key = '205347dac04e47b992a3a61613134f48'
    endpoint = f'https://api.opencagedata.com/geocode/v1/json?q={location}&key={api_key}'

    try:
        opnom  = OpcgGeocodeaddress()
        results = opnom.geocode(location)
        # print("opncage",results)
        return  results[0]['geometry']['lat'],results[0]['geometry']['lng']
        response = requests.get(endpoint)
        data = response.json()
        print("opncage",data)
        
        if data['results']:
            # Assuming you want the first result
            lat = data['results'][0]['geometry']['lat']
            lng = data['results'][0]['geometry']['lng']
            return lat, lng
        else:
            return None, None
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coordinates: {e}")
        return None, None

def  MapQuest_for_address(address):
    api_key = 'YOUR_MAPQUEST_API_KEY'
    url = f'http://www.mapquestapi.com/geocoding/v1/address?key={api_key}&location={address}'
    response = requests.get(url)
    data = response.json()
    if data['info']['statuscode'] == 0:
        location = data['results'][0]['locations'][0]['latLng']
        return location['lat'], location['lng']
    else:
        raise ValueError('Error in geocoding request')


def get_geocode(address):
    gmaps = googlemaps.Client(key="AIzaSyDhiqTpfrij_CvG-Xc7G-43Q_4Ezy0_lcw")
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        return location['lat'], location['lng']
    return None, None



def get_lat_lon_from_address(address, user_agent="ktkasad414@gmail.com"):
    """
    Get the latitude and longitude for a given address using Nominatim API.

    :param address: The address to geocode.
    :param user_agent: A User-Agent string to identify your application.
    :return: A tuple (latitude, longitude) if successful, otherwise None.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': address,
        'format': 'json',
        'limit': 1,
    }
    headers = {
        'User-Agent': user_agent,
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data:
            latitude = data[0].get('lat')
            longitude = data[0].get('lon')
            return float(latitude), float(longitude)
    except requests.RequestException as e:
        print(f"Error fetching data from Nominatim: {e}")
    return None,None



def  lat_long_nearest_admin(latitude,longitude): 
    radlat = Radians(latitude) # given latitude
    radlong = Radians(longitude) # given longitude
    radflat = Radians(F('latitude'))
    radflong = Radians(F('longitude')) 
    # 6371 is  Radius of the earth in km
    # 3959 is  Radius of the earth in miles
    Expression = 3959.0 * Acos(Cos(radlat) * Cos(radflat) * (Cos(radflong - radlong)) +  (Sin(radlat) * Sin(radflat))) 
    resturnts_yep = AdminAddress.objects.annotate(distance=Expression).exclude(latitude=None).exclude(longitude=None).order_by('distance').values_list('admin_address_id','distance')
    if resturnts_yep:
        for lat_calc in resturnts_yep:
            print("lat_calc",lat_calc)
            # for lar_k,lar_v in lat_calc.items():

            #     print("orig",lar_k,lar_v) 

        return resturnts_yep[0][0]
    else:
        return None

# def  lat_long_nearest_kitchen(latitude,longitude): 
#     radlat = Radians(latitude) # given latitude
#     radlong = Radians(longitude) # given longitude
#     radflat = Radians(F('latitude'))
#     radflong = Radians(F('longitude')) 
#     # 6371 is  Radius of the earth in km
#     # 3959 is  Radius of the earth in miles
#     Expression = 3959.0 * Acos(Cos(radlat) * Cos(radflat) * (Cos(radflong - radlong)) +  (Sin(radlat) * Sin(radflat))) 
    

#     # Exclude  pending and inactive kitchens
#     pending_inactive_kitchens = list(Kitchen.objects.filter(Q(status="pending") | Q(is_active=False)).values_list('pk',flat=True))
#     resturnts_yep = KitchenAddress.objects.annotate(distance=Expression).exclude(latitude=None).exclude(longitude=None).exclude(Kitchen_id__in=pending_inactive_kitchens).order_by('distance').values_list('Kitchen_id','distance')
#     if resturnts_yep:
#         for lat_calc in resturnts_yep:
#             print("lat_calc",lat_calc)
#             # for lar_k,lar_v in lat_calc.items():

#             #     print("orig",lar_k,lar_v) 

#         return resturnts_yep[0][0]
#     else:
#         return None




def  lat_long_nearest_kitchen(latitude,longitude): 

    print("Here in lat_long_nearest_kitchen function ")
    radlat = Radians(latitude) # given latitude
    radlong = Radians(longitude) # given longitude
    radflat = Radians(F('latitude'))
    radflong = Radians(F('longitude')) 
    # 6371 is  Radius of the earth in km
    # 3959 is  Radius of the earth in miles
    Expression = 6371.0 * Acos(Cos(radlat) * Cos(radflat) * (Cos(radflong - radlong)) +  (Sin(radlat) * Sin(radflat))) 
    if  FoodappSettings.objects.exists():
        foodapp_instance = FoodappSettings.objects.first()
        max_order_radius = foodapp_instance.orders_radius
    else:
        max_order_radius = 50

    # far kitchens list may be active or inactive
    print("check far kitchen ")
    
    in_range_kitchens = list(KitchenAddress.objects.annotate(distance=Expression).exclude(latitude=None).exclude(longitude=None).exclude(distance__gt= max_order_radius).values_list('Kitchen_id', flat=True))
    print("list of in range kichens", in_range_kitchens)
    if len(in_range_kitchens):
        pass
    else:
        return 3276,"other"

    # Exclude  pending and inactive kitchens
    pending_inactive_kitchens = list(Kitchen.objects.filter(Q(status="pending") | Q(is_active=False)).values_list('pk',flat=True))

    resturnts_yep = KitchenAddress.objects.annotate(distance=Expression).exclude(latitude=None).exclude(longitude=None).exclude(Kitchen_id__in=pending_inactive_kitchens).filter(Kitchen_id__in=in_range_kitchens).order_by('distance').values_list('Kitchen_id','distance')
    print("check chekc resturnts_yep",resturnts_yep)

    
    if resturnts_yep:

        # for lat_calc in resturnts_yep:
        #     print("lat_calc",lat_calc)
            # for lar_k,lar_v in lat_calc.items():

            #     print("orig",lar_k,lar_v) 
        # if resturnts_yep[0][1] > max_order_radius:
        #     print("Not Operate in Your Area")
        #     return 123
        # else:
        return resturnts_yep[0][0], resturnts_yep[0][1]
    else:
        #print("Unfortunatly today kitchen in Your area is inactive so we are not operating in your area today")
        return None, None



def get_lat_long_nominatim():
    # find lat and long from address

    nom =  Geocodeaddress()
    # sg = 'G972+7J6, MM Alam Rd, Block B1 Block B 1 Gulberg III'
    # jggh = 'Apartment #20'
    # gkj = 'Lahore'
    # fhgh = 'Punjab'
    # hgfhg = '54660'
    # state_zip = fhgh + ' ' + hgfhg
    # lmgj = 'Pakistan'

    sg = '2301 Grand Ave'
    jggh = 'Apartment #20'
    gkj = 'Hoover'
    fhgh = 'AL'
    hgfhg = '35226'
    state_zip = fhgh + ' ' + hgfhg
    lmgj = 'United States'  

    wholefhfh = [sg,gkj,state_zip,lmgj] 
    #lil = ','.join([n for n in wholefhfh]) 
    lil = "394 Street 15, Chaklala Scheme 3 Chaklala Housing Scheme 3, Rawalpindi, Punjab 46000, Pakistan"
    #lil  = "402 Street 15, Chaklala Scheme 3 Chaklala Housing Scheme 3, Rawalpindi, Punjab 46000, Pakistan"

    # print("lil tet",lil) 
    location_ab = nom.geocode(lil)
    # print("location_ab check",location_ab) 
    if location_ab is None:
        print("nominatim address can't found")
    else:
        # print("loc_ad",location_ab.address)
        print("latng--ad",(location_ab.latitude, location_ab.longitude))


    return True



def  lat_long_nearest_rider(latitude,longitude): 
    radlat = Radians(latitude) # given latitude
    radlong = Radians(longitude) # given longitude
    radflat = Radians(F('latitude'))
    radflong = Radians(F('longitude')) 
    # 6371 is  Radius of the earth in km
    # 3959 is  Radius of the earth in miles
    Expression = 6371.0 * Acos(Cos(radlat) * Cos(radflat) * (Cos(radflong - radlong)) +  (Sin(radlat) * Sin(radflat))) 
    resturnts_yep = RiderDetails.objects.annotate(distance=Expression).exclude(latitude=None).exclude(longitude=None).exclude(pk__in=list(RiderOrders.objects.filter(is_delivered=0).values_list('rider_id',flat=True))).exclude(is_active=False).order_by('distance').values_list('pk','distance')
    if resturnts_yep:
        for lat_calc in resturnts_yep:
            print("lat_calc",lat_calc)
            # for lar_k,lar_v in lat_calc.items():

            #     print("orig",lar_k,lar_v) 

        return resturnts_yep[0][0], resturnts_yep[0][1]
    else:
        return None, None
    

def  distance_in_km(latitude,longitude,lat_b,long_b):
    radlat = Radians(latitude) # given latitude
    radlong = Radians(longitude) # given longitude
    radflat = Radians(lat_b)
    radflong = Radians(long_b) 
    Expression = 6371.0 * Acos(Cos(radlat) * Cos(radflat) * (Cos(radflong - radlong)) +  (Sin(radlat) * Sin(radflat)))
    return   Expression



def  lat_long_forced_rider(latitude,longitude,rider_id): 
    radlat = Radians(latitude) # given latitude
    radlong = Radians(longitude) # given longitude
    radflat = Radians(F('latitude'))
    radflong = Radians(F('longitude')) 
    # 6371 is  Radius of the earth in km
    # 3959 is  Radius of the earth in miles
    Expression = 6371.0 * Acos(Cos(radlat) * Cos(radflat) * (Cos(radflong - radlong)) +  (Sin(radlat) * Sin(radflat))) 
    resturnts_yep = RiderDetails.objects.annotate(distance=Expression).exclude(latitude=None).exclude(longitude=None).filter(pk=rider_id).order_by('distance').values_list('pk','distance')
    if resturnts_yep:
        for lat_calc in resturnts_yep:
            print("lat_calc",lat_calc)
            # for lar_k,lar_v in lat_calc.items():

            #     print("orig",lar_k,lar_v) 

        return resturnts_yep[0][0], resturnts_yep[0][1]
    else:
        return None, None