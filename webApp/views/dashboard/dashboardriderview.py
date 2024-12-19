from django.shortcuts import render,redirect, HttpResponseRedirect
from webApp.models import *
from django.contrib import messages
from django.core.paginator import Paginator
from geopy.geocoders import Nominatim
from django.http import JsonResponse
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth import logout
from webApp.templatetags.webApp_extras import user_role
import json
import secrets
import string
from webApp.views.Others.geocode_address import *
from webApp.utils import *


def RiderCommisionForm(request):
    if RiderComissionsettings.objects.exists():
        re_render = False
        rider_commision_instance = RiderComissionsettings.objects.first()
        print(rider_commision_instance)

        context= {'re_render':re_render,'rider_commision_instance':rider_commision_instance}
        

    else:
        new_record = True
        context= {'new_record':new_record}


    return render(request, 'dashboard/Rider_Setting/edit_rider_comission_form.html', context)



def EditRiderCommisionForm(request):
    if request.method == 'POST':

        rider_commision_distance = request.POST.get('rider_commision_distance') or None
        print("rider_commision_distance",rider_commision_distance)

        if rider_commision_distance is None:
            user_added_warning = 'Please enter distance value!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        rider_commision_amount = request.POST.get('rider_commision_amount') or None
        print("rider_commision_amount",rider_commision_amount)

        if rider_commision_amount is None:
            user_added_warning = 'Please enter commision value!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        

        
        if RiderComissionsettings.objects.exists():

            rider_commision_instance = RiderComissionsettings.objects.first()
            rider_commision_instance.by_distance = rider_commision_distance
            rider_commision_instance.amount_share = rider_commision_amount

            rider_commision_instance.save()
        else:
            RiderComissionsettings.objects.create(by_distance = rider_commision_distance, amount_share = rider_commision_amount)


        group_added_success = 'Rider setting updated successfully !'  
        messages.success(request, group_added_success)
            
        return redirect(request.META.get('HTTP_REFERER'))