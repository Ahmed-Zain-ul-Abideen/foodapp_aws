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
from webApp.views.expo_notif_view import send_salient_data_message, send_push_message
from  fcm_django.models  import FCMDevice

def generate_random_string_secure(length):
    letters = string.ascii_letters + string.digits
    result_str = ''.join(secrets.choice(letters) for _ in range(length))
    return result_str

# Search kitchen
def  KitchenCustomSearch(request): 
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    
    if request.user.is_superuser:
        print("here in kitchen custom search")
        kitchen = request.GET.get('kitchen') or None   
        print("kitchen", kitchen)
        searched_kitchen_exist = Kitchen.objects.filter(name__icontains=kitchen).exists()
        if searched_kitchen_exist:    
            searched_kitchen = list(Kitchen.objects.filter(name__icontains=kitchen).values()) 
            print("list of kitchens",searched_kitchen) 
            
            context = {'ven':  searched_kitchen}  
            return JsonResponse({"success": True,"response":context}) 
        else:  
            return JsonResponse({"success": False})
    elif 'Kitchens'  in chk :
        print("here in kitchen custom search plus admin")
        kitchen = request.GET.get('kitchen') or None   
        print("kitchen", kitchen)
        searched_kitchen_exist = Kitchen.objects.filter(name__icontains=kitchen).filter(kitchen_admin=request.user.id).exists()
        if searched_kitchen_exist:    
            searched_kitchen = list(Kitchen.objects.filter(name__icontains=kitchen).filter(kitchen_admin=request.user.id).values()) 
            print("list of kitchens",searched_kitchen) 
            
            context = {'ven':  searched_kitchen}  
            return JsonResponse({"success": True,"response":context}) 
        else:  
            return JsonResponse({"success": False})

    else:
        return render(request, 'dashboard/permission_denied.html')



def AddKitchenForm(request,add_button_clicked=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Kitchens'  in chk or request.user.is_superuser:

        re_render = False

        if add_button_clicked:
            if '_old_post' in  request.session:
                del request.session['_old_post']    
                request.session['_old_post'] = None

        old_post = request.session.get('_old_post')
        print("data in old post is", old_post)

        if old_post is not None:

            re_render = True
            context= {'re_render':re_render, 
                    'kitchen_title': old_post['kitchen_title'], 
                    'kitchen_owner_name': old_post['kitchen_owner_name'],
                    'kitchen_owner_contact_number': old_post['kitchen_owner_contact_number'],
                    'kitchen_owner_email': old_post['kitchen_owner_email'],
                    'address_details': old_post['address_details'],
                    }
            

        else:
            context= {'re_render':re_render}
        return render(request, 'dashboard/Kitchens/add_kitchen_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')
    


def AddKitchen(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Kitchens'  in chk  or request.user.is_superuser:
        
        
        if request.method == 'POST':
            re_render = False
            post_data = request.POST

            address_details = request.POST.get('address_details') or None
            kitchen_name = request.POST.get('kitchen_title') or None
            print("kitchen_name",kitchen_name)
            
            


            if address_details is None:
                kitchen_added_warning = 'Please enter complete address!'  
                messages.warning(request, kitchen_added_warning) 
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['kitchen_title'] = post_data['kitchen_title']
                old_data['address_details'] = post_data['address_details']
                old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                # old_data['street_address_1'] = post_data['street_address_1']

                # old_data['address_city'] = post_data['address_city'] or None
                # old_data['address_postcode'] = post_data['address_postcode'] or None
                
                

                print("old data", old_data)
                request.session['_old_post'] = old_data 
                return HttpResponseRedirect('add_kitchen_form/0') 
            elif not address_details: 
                kitchen_added_warning = 'Empty address is not allowed !'  
                messages.warning(request, kitchen_added_warning) 
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['kitchen_title'] = post_data['kitchen_title']
                old_data['address_details'] = post_data['address_details']
                old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                # old_data['street_address_1'] = post_data['street_address_1']

                # old_data['address_city'] = post_data['address_city'] or None
                # old_data['address_postcode'] = post_data['address_postcode'] or None
                
                

                print("old data", old_data)
                request.session['_old_post'] = old_data 
                return HttpResponseRedirect('add_kitchen_form/0') 
            
            try:
                lat, long = OpenCage_for_address(address_details)
            except:
                kitchen_added_warning = 'This address cannot be located please enter valiid one !'  
                messages.warning(request, kitchen_added_warning) 
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['kitchen_title'] = post_data['kitchen_title']
                old_data['address_details'] = post_data['address_details']
                old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                # old_data['street_address_1'] = post_data['street_address_1']

                # old_data['address_city'] = post_data['address_city'] or None
                # old_data['address_postcode'] = post_data['address_postcode'] or None
                
                

                print("old data", old_data)
                request.session['_old_post'] = old_data 
                return HttpResponseRedirect('add_kitchen_form/0') 
                 
            print("lat opncg,long opncg",lat,long)
            if lat is None:
                kitchen_added_warning = 'This address cannot be located please enter valiid one !'  
                messages.warning(request, kitchen_added_warning) 
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['kitchen_title'] = post_data['kitchen_title']
                old_data['address_details'] = post_data['address_details']
                old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                # old_data['street_address_1'] = post_data['street_address_1']

                # old_data['address_city'] = post_data['address_city'] or None
                # old_data['address_postcode'] = post_data['address_postcode'] or None
                
                

                print("old data", old_data)
                request.session['_old_post'] = old_data 
                return HttpResponseRedirect('add_kitchen_form/0') 
            
            
            
            if kitchen_name is None:
                kitchen_added_warning = 'Please enter kitchen name !'  
                messages.warning(request, kitchen_added_warning) 
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['kitchen_title'] = post_data['kitchen_title']
                old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                old_data['address_details'] = post_data['address_details']

                # old_data['address_city'] = post_data['address_city'] or None
                # old_data['address_postcode'] = post_data['address_postcode'] or None
                
                

                print("old data", old_data)
                request.session['_old_post'] = old_data 
                return HttpResponseRedirect('add_kitchen_form/0') 
                # return redirect(request.META.get('HTTP_REFERER'))
            else:
                    if not kitchen_name:
                        kitchen_added_warning = 'Empty kitchen name not allowed !'  
                        messages.warning(request, kitchen_added_warning) 
                        if '_old_post' in  request.session:
                            del request.session['_old_post']
                        old_data = {}
                        old_data['kitchen_title'] = post_data['kitchen_title']
                        old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                        old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                        old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                        old_data['address_details'] = post_data['address_details']

                        # old_data['address_city'] = post_data['address_city'] or None
                        # old_data['address_postcode'] = post_data['address_postcode'] or None
                        
                        

                        print("old data", old_data)
                        request.session['_old_post'] = old_data 
                        return HttpResponseRedirect('add_kitchen_form/0') 

            owner_name = request.POST.get('kitchen_owner_name') or None
            print("owner_name",owner_name)

            if owner_name is None:
                kitchen_added_warning = 'Please enter owner name !'  
                messages.warning(request, kitchen_added_warning) 
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['kitchen_title'] = post_data['kitchen_title']
                old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                old_data['address_details'] = post_data['address_details']

                # old_data['address_city'] = post_data['address_city'] or None
                # old_data['address_postcode'] = post_data['address_postcode'] or None
                
                

                print("old data", old_data)
                request.session['_old_post'] = old_data 
                return HttpResponseRedirect('add_kitchen_form/0') 
                # return redirect(request.META.get('HTTP_REFERER'))
            else:
                    if not owner_name:
                        kitchen_added_warning = 'Empty owner name not allowed !'  
                        messages.warning(request, kitchen_added_warning) 
                        if '_old_post' in  request.session:
                                del request.session['_old_post']
                        old_data = {}
                        old_data['kitchen_title'] = post_data['kitchen_title']
                        old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                        old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                        old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                        old_data['address_details'] = post_data['address_details']

                        # old_data['address_city'] = post_data['address_city'] or None
                        # old_data['address_postcode'] = post_data['address_postcode'] or None
                        
                        

                        print("old data", old_data)
                        request.session['_old_post'] = old_data 
                        return HttpResponseRedirect('add_kitchen_form/0') 
                        # return redirect(request.META.get('HTTP_REFERER'))
                    
            contact_number = request.POST.get('kitchen_owner_contact_number') or None
            print("contact_number",contact_number)
            if contact_number is None:
                kitchen_added_warning = 'Please enter contact number !'  
                messages.warning(request, kitchen_added_warning) 
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['kitchen_title'] = post_data['kitchen_title']
                old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                old_data['address_details'] = post_data['address_details']

                # old_data['address_city'] = post_data['address_city'] or None
                # old_data['address_postcode'] = post_data['address_postcode'] or None
                
                

                print("old data", old_data)
                request.session['_old_post'] = old_data 
                return HttpResponseRedirect('add_kitchen_form/0') 
                # return redirect(request.META.get('HTTP_REFERER'))
            else:
                    if not contact_number:
                        kitchen_added_warning = 'Empty contact number not allowed !'  
                        messages.warning(request, kitchen_added_warning) 
                        if '_old_post' in  request.session:
                                del request.session['_old_post']
                        old_data = {}
                        old_data['kitchen_title'] = post_data['kitchen_title']
                        old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                        old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                        old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                        old_data['address_details'] = post_data['address_details']

                        # old_data['address_city'] = post_data['address_city'] or None
                        # old_data['address_postcode'] = post_data['address_postcode'] or None
                        
                        

                        print("old data", old_data)
                        request.session['_old_post'] = old_data 
                        return HttpResponseRedirect('add_kitchen_form/0') 
                        # return redirect(request.META.get('HTTP_REFERER'))
                    
            email = request.POST.get('kitchen_owner_email') or None
            print("email",email)
            if email is None:
                kitchen_added_warning = 'Please enter email !'  
                messages.warning(request, kitchen_added_warning) 
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['kitchen_title'] = post_data['kitchen_title']
                old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                old_data['address_details'] = post_data['address_details']

                # old_data['address_city'] = post_data['address_city'] or None
                # old_data['address_postcode'] = post_data['address_postcode'] or None
                
                

                print("old data", old_data)
                request.session['_old_post'] = old_data 
                return HttpResponseRedirect('add_kitchen_form/0') 
                # return redirect(request.META.get('HTTP_REFERER'))
            else:
                if not email:
                    kitchen_added_warning = 'Empty email not allowed !'  
                    messages.warning(request, kitchen_added_warning)
                    if '_old_post' in  request.session:
                            del request.session['_old_post']
                    old_data = {}
                    old_data['kitchen_title'] = post_data['kitchen_title']
                    old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                    old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                    old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                    old_data['address_details'] = post_data['address_details']

                    # old_data['address_city'] = post_data['address_city'] or None
                    # old_data['address_postcode'] = post_data['address_postcode'] or None
                    
                    

                    print("old data", old_data)
                    request.session['_old_post'] = old_data 
                    return HttpResponseRedirect('add_kitchen_form/0')  
                    # return redirect(request.META.get('HTTP_REFERER'))



            if  verify_email_smtp(email):
                pass
            else:

                kitchen_added_warning = 'This email is not deliverable !'  
                messages.warning(request, kitchen_added_warning) 
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['kitchen_title'] = post_data['kitchen_title']
                old_data['address_details'] = post_data['address_details']
                old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                # old_data['street_address_1'] = post_data['street_address_1']

                # old_data['address_city'] = post_data['address_city'] or None
                # old_data['address_postcode'] = post_data['address_postcode'] or None
                
                

                # print("old data", old_data)
                request.session['_old_post'] = old_data 
                return HttpResponseRedirect('add_kitchen_form/0') 

            try:
                context = {'user_name': owner_name,'kitchen_name':kitchen_name}
                send_html_email('Welcome to Food App',  email, context,'dashboard/Emails/welcomemail.html')
            except Exception as e:
                print("mail e",e)
                kitchen_added_warning = 'This email is not reachable !'  
                messages.warning(request, kitchen_added_warning) 
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['kitchen_title'] = post_data['kitchen_title']
                old_data['address_details'] = post_data['address_details']
                old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                # old_data['street_address_1'] = post_data['street_address_1']

                # old_data['address_city'] = post_data['address_city'] or None
                # old_data['address_postcode'] = post_data['address_postcode'] or None
                
                

                print("old data", old_data)
                request.session['_old_post'] = old_data 
                return HttpResponseRedirect('add_kitchen_form/0') 
                    
            # street_address = request.POST.get('street_address_1') or None
            # print("street_address",street_address)
            # if street_address is None:
            #     kitchen_added_warning = 'Please enter street address !'  
            #     messages.warning(request, kitchen_added_warning) 
            #     if '_old_post' in  request.session:
            #             del request.session['_old_post']
            #     old_data = {}
            #     old_data['kitchen_title'] = post_data['kitchen_title']
            #     old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
            #     old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
            #     old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
            #     old_data['street_address_1'] = post_data['street_address_1']

            #     old_data['address_city'] = post_data['address_city'] or None
            #     old_data['address_postcode'] = post_data['address_postcode'] or None
                
                

            #     print("old data", old_data)
            #     request.session['_old_post'] = old_data 
            #     return HttpResponseRedirect('add_kitchen_form/0') 
            #     # return redirect(request.META.get('HTTP_REFERER'))
            # else:
            #         if not street_address:
            #             kitchen_added_warning = 'Empty street address not allowed !'  
            #             messages.warning(request, kitchen_added_warning) 
            #             if '_old_post' in  request.session:
            #                     del request.session['_old_post']
            #             old_data = {}
            #             old_data['kitchen_title'] = post_data['kitchen_title']
            #             old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
            #             old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
            #             old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
            #             old_data['street_address_1'] = post_data['street_address_1']

            #             old_data['address_city'] = post_data['address_city'] or None
            #             old_data['address_postcode'] = post_data['address_postcode'] or None
                        
                        

            #             print("old data", old_data)
            #             request.session['_old_post'] = old_data 
            #             return HttpResponseRedirect('add_kitchen_form/0') 
            #             # return redirect(request.META.get('HTTP_REFERER'))

            # address_city = request.POST.get('address_city') or None
            # print("address_city",address_city)
            # if address_city is None:
            #     kitchen_added_warning = 'Please enter city name !'  
            #     messages.warning(request, kitchen_added_warning) 
            #     if '_old_post' in  request.session:
            #             del request.session['_old_post']
            #     old_data = {}
            #     old_data['kitchen_title'] = post_data['kitchen_title']
            #     old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
            #     old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
            #     old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
            #     old_data['street_address_1'] = post_data['street_address_1']

            #     old_data['address_city'] = post_data['address_city'] or None
            #     old_data['address_postcode'] = post_data['address_postcode'] or None
                
                

            #     print("old data", old_data)
            #     request.session['_old_post'] = old_data 
            #     return HttpResponseRedirect('add_kitchen_form/0') 
            #     # return redirect(request.META.get('HTTP_REFERER'))
            # else:
            #         if not address_city:
            #             kitchen_added_warning = 'Empty city name not allowed !'  
            #             messages.warning(request, kitchen_added_warning) 
            #             if '_old_post' in  request.session:
            #                     del request.session['_old_post']
            #             old_data = {}
            #             old_data['kitchen_title'] = post_data['kitchen_title']
            #             old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
            #             old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
            #             old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
            #             old_data['street_address_1'] = post_data['street_address_1']

            #             old_data['address_city'] = post_data['address_city'] or None
            #             old_data['address_postcode'] = post_data['address_postcode'] or None
                        
                        

            #             print("old data", old_data)
            #             request.session['_old_post'] = old_data 
            #             return HttpResponseRedirect('add_kitchen_form/0') 
            #             # return redirect(request.META.get('HTTP_REFERER'))


            # address_postcode = request.POST.get('address_postcode') or None
            # print("address_postcode",address_postcode)
            # if address_postcode is None:
            #     kitchen_added_warning = 'Please enter postal code !'  
            #     messages.warning(request, kitchen_added_warning)
            #     if '_old_post' in  request.session:
            #             del request.session['_old_post']
            #     old_data = {}
            #     old_data['kitchen_title'] = post_data['kitchen_title']
            #     old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
            #     old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
            #     old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
            #     old_data['street_address_1'] = post_data['street_address_1']

            #     old_data['address_city'] = post_data['address_city'] or None
            #     old_data['address_postcode'] = post_data['address_postcode'] or None
                
                

            #     print("old data", old_data)
            #     request.session['_old_post'] = old_data 
            #     return HttpResponseRedirect('add_kitchen_form/0')  
            #     # return redirect(request.META.get('HTTP_REFERER'))
            # else:
            #         if not address_postcode:
            #             kitchen_added_warning = 'Empty postal code not allowed !'  
            #             messages.warning(request, kitchen_added_warning) 
            #             if '_old_post' in  request.session:
            #                     del request.session['_old_post']
            #             old_data = {}
            #             old_data['kitchen_title'] = post_data['kitchen_title']
            #             old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
            #             old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
            #             old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
            #             old_data['street_address_1'] = post_data['street_address_1']

            #             old_data['address_city'] = post_data['address_city'] or None
            #             old_data['address_postcode'] = post_data['address_postcode'] or None
                        
                        

            #             print("old data", old_data)
            #             request.session['_old_post'] = old_data 
            #             return HttpResponseRedirect('add_kitchen_form/0') 
                        # return redirect(request.META.get('HTTP_REFERER'))
                    
            kitchen_images = request.FILES.getlist('kitchen_images') or None
            print("kitchen_images",kitchen_images)

            if kitchen_images is None:
                kitchen_added_warning = 'Please uplaod kitchen images !'  
                messages.warning(request, kitchen_added_warning)
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['kitchen_title'] = post_data['kitchen_title']
                old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                old_data['address_details'] = post_data['address_details']

                # old_data['address_city'] = post_data['address_city'] or None
                # old_data['address_postcode'] = post_data['address_postcode'] or None
                
                

                print("old data", old_data)
                request.session['_old_post'] = old_data 
                return HttpResponseRedirect('add_kitchen_form/0') 
                # return redirect(request.META.get('HTTP_REFERER'))

            if kitchen_images:

                for image in kitchen_images:

                    file_extension = image.name.split('.')[-1].lower()
                    print("file extention", file_extension)
                
                    if file_extension in ['png', 'jpg', 'jpeg']:
                        pass
                    else:
                        name_added_warning = 'Uplaod image file Only !'  
                        messages.warning(request, name_added_warning) 
                        if '_old_post' in  request.session:
                                del request.session['_old_post']
                        old_data = {}
                        old_data['kitchen_title'] = post_data['kitchen_title']
                        old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                        old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                        old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                        old_data['address_details'] = post_data['address_details']

                        # old_data['address_city'] = post_data['address_city'] or None
                        # old_data['address_postcode'] = post_data['address_postcode'] or None
                        
                        

                        print("old data", old_data)
                        request.session['_old_post'] = old_data 
                        return HttpResponseRedirect('add_kitchen_form/0')   
                        # return redirect(request.META.get('HTTP_REFERER'))

            

            try:
                kitchen_admin = lat_long_nearest_admin(lat,long)
            except:
                kitchen_admin = None

            print("kitchen_admin",kitchen_admin)

            if Kitchen.objects.filter(name = kitchen_name).exists():
                
                return HttpResponseRedirect('add_kitchen_form/0')
            else:
                 

                kitchen_instance = Kitchen.objects.create(kitchen_admin=kitchen_admin,name= kitchen_name, owner= owner_name , contact = contact_number, email = email)

                kitchen_instance.save()

                kitchenAddress_instance = KitchenAddress.objects.create(Kitchen = kitchen_instance ,address_details= address_details,latitude=lat,longitude=long)
                kitchenAddress_instance.save() 

                # kitchenAddress_instance = KitchenAddress.objects.create(Kitchen = kitchen_instance ,address_line1= street_address, city= address_city , postal_code= address_postcode , country = 'Pakistan')
                # kitchenAddress_instance.save()

                # full_address = kitchenAddress_instance.full_address()
                # print("full_address",full_address, type(full_address))


                # geolocator = Nominatim(user_agent="webApp")
                # location_cord = geolocator.geocode(full_address)
                # print ("location_cord", location_cord)

                # kitchenAddress_instance.latitude = location_cord.latitude
                # kitchenAddress_instance.longitude = location_cord.longitude
                # kitchenAddress_instance.save()


                for image in kitchen_images:
                    KitchenMedia.objects.create(Kitchen = kitchen_instance ,file=image)

                kitchen_added_success = 'Kitchen' + ' ' + kitchen_instance.name + ' ' + 'added successfully !'  
                messages.success(request, kitchen_added_success)
                if '_old_post' in  request.session:
                    del request.session['_old_post']    
                request.session['_old_post'] = None
                return HttpResponseRedirect('add_kitchen_form/1')


            return render(request, 'dashboard/Kitchens/add_kitchen_form.html')
    else:
        return render(request, 'dashboard/permission_denied.html') 



def  MyKitchenOrdersList(request):  
    chk = user_role(request.user)
    if len(chk) == 0:
      return redirect('login-dashboard')  
    elif len(chk) == 1 :
      return render(request, 'dashboard/permission_denied_updt.html')
    else: 
        if Kitchen.objects.filter(approved_owner_id=request.user.id).exists():
            all_order_status = Orderstatus.objects.filter(role = 'Kitchen').all()
            my_kitchen = Kitchen.objects.filter(approved_owner_id=request.user.id).first()
            if  not   Orders.objects.filter(kitchen_id=my_kitchen.id).exists() :
                context = {'ven': "Not Found"}
            else: 
                paginator = Paginator(Orders.objects.filter(kitchen_id=my_kitchen.id).exclude(status = "to_be_confirmed").order_by('-id'), 15)
                page = request.GET.get('page')
                paginated_items = paginator.get_page(page)
                context= {'ven': paginated_items,'my_kitchen':my_kitchen,'all_order_status':all_order_status}
             
        else:
            return render(request, 'dashboard/permission_denied_updt.html')
      
    return render(request, 'dashboard/Kitchens/my_kitchen_orders.html', context)


def  SelectKitchenSpecialities(request):  
    chk = user_role(request.user)
    if len(chk) == 0:
      return redirect('login-dashboard')  
    elif len(chk) == 1 :
      return render(request, 'dashboard/permission_denied_updt.html')
    else: 
        if Kitchen.objects.filter(approved_owner_id=request.user.id).exists():
            my_kitchen = Kitchen.objects.filter(approved_owner_id=request.user.id).first()
            if KitchenSpeciality.objects.filter(Kitchen_id=my_kitchen.id).exists() :
                kitchen_speciality_items = KitchenSpeciality.objects.filter(Kitchen_id=my_kitchen.id).first()
                kitchen_speciality_items = json.decoder.JSONDecoder().decode(kitchen_speciality_items.items)
            else:
                kitchen_speciality_items = []
            if Menuitems.objects.exists(): 
                paginator = Paginator(Menuitems.objects.filter(daily_deals = True).all().order_by('-id'), 15)
                page = request.GET.get('page')
                paginated_items = paginator.get_page(page)
                context= {'ven': paginated_items,'my_kitchen':my_kitchen,'kitchen_speciality_items':kitchen_speciality_items}
            else:
                context = {'ven': "Not Found"}
        else:
            return render(request, 'dashboard/permission_denied_updt.html')
      
    return render(request, 'dashboard/Kitchens/select_kitchen_speciality.html', context)

def UpdateKitchenStatus(request):
    
    
    my_ktch = request.GET.get("my_ktch")
    print('my_ktch',my_ktch)
    kitxhen = Kitchen.objects.filter(pk=my_ktch).first()
    kitxhen.status = "Approved"
    kitxhen.save()
    if  FCMDevice.objects.filter(user_id= kitxhen.approved_owner.pk).filter(active=True).exists():
        fcm_device_instance = FCMDevice.objects.filter(user_id= kitxhen.approved_owner.pk).filter(active=True)
        for  device  in fcm_device_instance:
            token = device.registration_id

            print("token",token)
            message = 'Your kitchen status is approved! Get ready for new orders.'  
            # send push notification 
            try:
                extra = {"link": "/(tabs)/home"}
                send_push_message(token, message, extra)
                print("messaged sent")
            except:
                print("messaged not  sent to kitchen app device",device.registration_id)

            # send data notification
            try:
                extra = {"newData": "2"}
                send_salient_data_message(token, extra)
            except Exception as e:
                print("Error:", e)

    # embed_id = generate_random_string_secure(4) + str(kitxhen.pk) + generate_random_string_secure(4)
    # link_for_registration = "http://localhost:8000/register_chef/" + embed_id 
    # de_embed = embed_id[4:]
    # de_embed = de_embed[:-4]
    # print("raned",embed_id,"    ") 

    try:
        context = {'user_name': kitxhen.owner,'kitchen_name':kitxhen.name}
        send_html_email('Kitchen Approved',  kitxhen.email, context,'dashboard/Emails/kitchen_signup.html')
    except Exception as e:
        print("mail e",e)

    data = {'resp_message': "kitchen status updated"}
    return JsonResponse(data) 


def SaveKitchenSpeciality(request):
    
    
    my_ktch = request.GET.get("my_ktch")
    id = request.GET.get("id")
    # print(my_ktch,id)
    if KitchenSpeciality.objects.filter(Kitchen_id=my_ktch).exists():
        kitchen_speciality_items = KitchenSpeciality.objects.filter(Kitchen_id=my_ktch).first()
        kitchen_speciality_items_list = json.decoder.JSONDecoder().decode(kitchen_speciality_items.items)
        if int(id) in kitchen_speciality_items_list:
            kitchen_speciality_items_list.remove(int(id))
        else:
            kitchen_speciality_items_list.append(int(id))

        kitchen_speciality_items.items = json.dumps(kitchen_speciality_items_list)
    else:
        kitchen_speciality_items = KitchenSpeciality.objects.create(Kitchen_id=my_ktch,items=json.dumps([int(id)]))
    
    kitchen_speciality_items.save() 

    data = {'resp_message': "item status updated"}
    return JsonResponse(data)


def SaveKitchenisactive(request):
    
    
    my_ktch = request.GET.get("my_ktch") 
    if Kitchen.objects.filter(pk=my_ktch).filter(is_active=True).exists(): 
        Kitchen.objects.filter(pk=my_ktch).update(is_active=False)
        data = {'resp_message': "Kitchen is set inactive"}
         
    else:
        Kitchen.objects.filter(pk=my_ktch).update(is_active=True)
        data = {'resp_message': "Kitchen is set active"}

   
    return JsonResponse(data)

def Kitchenlist(request):  
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group) 

    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    
    if request.user.is_superuser:
        all_kitchens = Kitchen.objects.all()
        if not all_kitchens:
            ven = "Not Found"
            
        else: 
            p = Paginator(Kitchen.objects.all().order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        context = {'ven':ven}
        print("checking alpha list",ven)
        return render(request, 'dashboard/Kitchens/index.html', context)
    
    elif 'Kitchens'  in chk :
    
        all_kitchens = Kitchen.objects.filter(kitchen_admin=request.user.id).exists()
        if not all_kitchens:
            ven = "Not Found"
            
        else: 
            p = Paginator(Kitchen.objects.filter(kitchen_admin=request.user.id).order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        context = {'ven':ven}
        print("checking alpha list",ven)
        return render(request, 'dashboard/Kitchens/index.html', context)
         
    else:
        return render(request, 'dashboard/permission_denied.html')
         


def DeleteKitchen(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Kitchens'  in chk or request.user.is_superuser:
    
        print("here for deleteing Kitchen record")
        kitchen_id = request.GET.get("kitchen_id")    
        print("kitchen_id", kitchen_id)
        kitchen_instance = Kitchen.objects.filter(id=kitchen_id).first()
        kitchen_name = kitchen_instance.name.title()

        kitchen_instance.delete() 
        print("record deleted Successfully!")
        data = {'kitchen_name':kitchen_name}
        return JsonResponse(data)
    else:
        return render(request, 'dashboard/permission_denied.html')


def EditKitchenForm(request,id,add_button_clicked=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Kitchens'  in chk or request.user.is_superuser:
        re_render = False
        kitchen = Kitchen.objects.filter(pk=id).first()
        kitchenaddress = KitchenAddress.objects.filter(Kitchen_id = id).first()



        if add_button_clicked:
            if '_old_post' in  request.session:
                del request.session['_old_post']    
                request.session['_old_post'] = None

        old_post = request.session.get('_old_post')
        print("data in old post is sub tile re render case ", old_post)

        if old_post is not None:

            re_render = True
            context= {'re_render':re_render,
                    'kitchen':kitchen, 
                    'KitchenAddress':kitchenaddress,
                    'kitchen_title': old_post['kitchen_title'], 
                    'kitchen_owner_name': old_post['kitchen_owner_name'],
                    'kitchen_owner_contact_number': old_post['kitchen_owner_contact_number'],
                    'kitchen_owner_email': old_post['kitchen_owner_email'],
                    'address_details': old_post['address_details'],
                    
                    }

        else:
            context= {'re_render':re_render,'kitchen':kitchen, 'KitchenAddress':kitchenaddress}
        return render(request, 'dashboard/Kitchens/edit_kitchen_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')





def EditKitchen(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'Kitchens'  in chk or request.user.is_superuser:
        if request.method == 'POST':

            re_render = False
            post_data = request.POST

            update_kitchen_pk = request.POST.get('update_kitchen_pk') or None
            print("update_kitchen_pk",update_kitchen_pk)
            lat = None
            send_mail = False


            kitchen_name = request.POST.get('kitchen_title') or None
            print("kitchen_name",kitchen_name)

            address_details = request.POST.get('address_details') or None 

            if address_details is None:
                kitchen_added_warning = 'Please enter complete address!'  
                messages.warning(request, kitchen_added_warning) 
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['kitchen_title'] = post_data['kitchen_title']
                old_data['address_details'] = post_data['address_details']
                old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                
                
                

                print("old data", old_data)
                request.session['_old_post'] = old_data 
                add_button_clicked = 0
                url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

                return HttpResponseRedirect(url)
            elif not address_details: 
                kitchen_added_warning = 'Empty address is not allowed !'  
                messages.warning(request, kitchen_added_warning) 
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['kitchen_title'] = post_data['kitchen_title']
                old_data['address_details'] = post_data['address_details']
                old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                
                
                

                print("old data", old_data)
                request.session['_old_post'] = old_data 
                add_button_clicked = 0
                url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

                return HttpResponseRedirect(url) 
            
             
            if KitchenAddress.objects.filter(Kitchen_id=update_kitchen_pk).filter(address_details=address_details).exists():
                print("same update address")
            else:
                try:
                    lat, long = OpenCage_for_address(address_details)
                except:
                    kitchen_added_warning = 'This address cannot be located please enter valid one !'  
                    messages.warning(request, kitchen_added_warning) 
                    if '_old_post' in  request.session:
                            del request.session['_old_post']
                    old_data = {}
                    old_data['kitchen_title'] = post_data['kitchen_title']
                    old_data['address_details'] = post_data['address_details']
                    old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                    old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                    old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                    
                    
                    

                    print("old data", old_data)
                    request.session['_old_post'] = old_data 
                    add_button_clicked = 0
                    url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

                    return HttpResponseRedirect(url)
                    
                print("lat opncg,long opncg",lat,long)
                if lat is None:
                    kitchen_added_warning = 'This address cannot be located please enter valid one !'  
                    messages.warning(request, kitchen_added_warning) 
                    if '_old_post' in  request.session:
                            del request.session['_old_post']
                    old_data = {}
                    old_data['kitchen_title'] = post_data['kitchen_title']
                    old_data['address_details'] = post_data['address_details']
                    old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                    old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                    old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                    
                    
                    

                    print("old data", old_data)
                    request.session['_old_post'] = old_data 
                    add_button_clicked = 0
                    url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

                    return HttpResponseRedirect(url) 
                
                send_mail = True

            if kitchen_name is None:
                kitchen_added_warning = 'Please enter kitchen name !'  
                messages.warning(request, kitchen_added_warning) 
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['kitchen_title'] = post_data['kitchen_title']
                old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                old_data['address_details'] = post_data['address_details']
                
                

                print("old data", old_data)
                request.session['_old_post'] = old_data 
                add_button_clicked = 0
                url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

                return HttpResponseRedirect(url)
                
                # return redirect(request.META.get('HTTP_REFERER'))
            else:
                    if not kitchen_name:
                        kitchen_added_warning = 'Empty kitchen name not allowed !'  
                        messages.warning(request, kitchen_added_warning) 
                        if '_old_post' in  request.session:
                            del request.session['_old_post']
                        old_data = {}
                        old_data['kitchen_title'] = post_data['kitchen_title']
                        old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                        old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                        old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                        old_data['address_details'] = post_data['address_details']
                        
                        

                        print("old data", old_data)
                        request.session['_old_post'] = old_data 
                        add_button_clicked = 0
                        url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

                        return HttpResponseRedirect(url)



            owner_name = request.POST.get('kitchen_owner_name') or None
            print("owner_name",owner_name)

            if owner_name is None:
                kitchen_added_warning = 'Please enter owner name !'  
                messages.warning(request, kitchen_added_warning) 
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['kitchen_title'] = post_data['kitchen_title']
                old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                old_data['address_details'] = post_data['address_details']
                print("old data", old_data)
                request.session['_old_post'] = old_data 
                add_button_clicked = 0
                url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

                return HttpResponseRedirect(url)
                
                # return redirect(request.META.get('HTTP_REFERER'))
            else:
                    if not owner_name:
                        kitchen_added_warning = 'Empty owner name not allowed !'  
                        messages.warning(request, kitchen_added_warning) 
                        if '_old_post' in  request.session:
                            del request.session['_old_post']
                        old_data = {}
                        old_data['kitchen_title'] = post_data['kitchen_title']
                        old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                        old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                        old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                        old_data['address_details'] = post_data['address_details']
                        print("old data", old_data)
                        request.session['_old_post'] = old_data 
                        add_button_clicked = 0
                        url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

                        return HttpResponseRedirect(url)
                    

            contact_number = request.POST.get('kitchen_owner_contact_number') or None
            print("contact_number",contact_number)
            if contact_number is None:
                kitchen_added_warning = 'Please enter contact number !'  
                messages.warning(request, kitchen_added_warning) 
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['kitchen_title'] = post_data['kitchen_title']
                old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                old_data['address_details'] = post_data['address_details']
                print("old data", old_data)
                request.session['_old_post'] = old_data 
                add_button_clicked = 0
                url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

                return HttpResponseRedirect(url)
                
                # return redirect(request.META.get('HTTP_REFERER'))
            else:
                    if not contact_number:
                        kitchen_added_warning = 'Empty contact number not allowed !'  
                        messages.warning(request, kitchen_added_warning) 
                        if '_old_post' in  request.session:
                            del request.session['_old_post']
                        old_data = {}
                        old_data['kitchen_title'] = post_data['kitchen_title']
                        old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                        old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                        old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                        old_data['address_details'] = post_data['address_details']
                        print("old data", old_data)
                        request.session['_old_post'] = old_data 
                        add_button_clicked = 0
                        url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

                        return HttpResponseRedirect(url)
                    
            email = request.POST.get('kitchen_owner_email') or None
            print("email",email)
            if email is None:
                kitchen_added_warning = 'Please enter email !'  
                messages.warning(request, kitchen_added_warning) 
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['kitchen_title'] = post_data['kitchen_title']
                old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                old_data['address_details'] = post_data['address_details']
                print("old data", old_data)
                request.session['_old_post'] = old_data 
                add_button_clicked = 0
                url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

                return HttpResponseRedirect(url)
                
                # return redirect(request.META.get('HTTP_REFERER'))
            else:
                    if not email:
                        kitchen_added_warning = 'Empty email not allowed !'  
                        messages.warning(request, kitchen_added_warning) 
                        if '_old_post' in  request.session:
                            del request.session['_old_post']
                        old_data = {}
                        old_data['kitchen_title'] = post_data['kitchen_title']
                        old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                        old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                        old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                        old_data['address_details'] = post_data['address_details']
                        print("old data", old_data)
                        request.session['_old_post'] = old_data 
                        add_button_clicked = 0
                        url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

                        return HttpResponseRedirect(url)
                    

            if Kitchen.objects.filter(pk=update_kitchen_pk).filter(email=email).exists():
                print("same email update")
            else:
                send_mail = True


            # print("ver smt em",verify_email_smtp(email))

            if send_mail:

                if  verify_email_smtp(email):
                    pass
                else:

                    kitchen_added_warning = 'This email is not deliverable !'  
                    messages.warning(request, kitchen_added_warning) 
                    if '_old_post' in  request.session:
                            del request.session['_old_post']
                    old_data = {}
                    old_data['kitchen_title'] = post_data['kitchen_title']
                    old_data['address_details'] = post_data['address_details']
                    old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                    old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                    old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                    
                    
                    

                    print("old data", old_data)
                    request.session['_old_post'] = old_data 
                    add_button_clicked = 0
                    url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

                    return HttpResponseRedirect(url)
                    
                try:
                    context = {'user_name': owner_name,'kitchen_name':kitchen_name}
                    send_html_email('Kitchen Info Updated',  email, context,'dashboard/Emails/kitchen_updated.html')
                except Exception as e:
                    print("mail e",e)
                    kitchen_added_warning = 'This email is not reachable !'  
                    messages.warning(request, kitchen_added_warning) 
                    if '_old_post' in  request.session:
                            del request.session['_old_post']
                    old_data = {}
                    old_data['kitchen_title'] = post_data['kitchen_title']
                    old_data['address_details'] = post_data['address_details']
                    old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
                    old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
                    old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
                    
                    
                    

                    print("old data", old_data)
                    request.session['_old_post'] = old_data 
                    add_button_clicked = 0
                    url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

                    return HttpResponseRedirect(url)
            # street_address = request.POST.get('street_address_1') or None
            # print("street_address",street_address)
            # if street_address is None:
            #     kitchen_added_warning = 'Please enter street address !'  
            #     messages.warning(request, kitchen_added_warning) 
            #     if '_old_post' in  request.session:
            #             del request.session['_old_post']
            #     old_data = {}
            #     old_data['kitchen_title'] = post_data['kitchen_title']
            #     old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
            #     old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
            #     old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
            #     old_data['street_address_1'] = post_data['street_address_1']
            #     old_data['address_city'] = post_data['address_city'] or None
            #     old_data['address_postcode'] = post_data['address_postcode'] or None
            #     print("old data", old_data)
            #     request.session['_old_post'] = old_data 
            #     add_button_clicked = 0
            #     url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

            #     return HttpResponseRedirect(url)
                
            #     # return redirect(request.META.get('HTTP_REFERER'))
            # else:
            #         if not street_address:
            #             kitchen_added_warning = 'Empty street address not allowed !'  
            #             messages.warning(request, kitchen_added_warning) 
            #             if '_old_post' in  request.session:
            #                 del request.session['_old_post']
            #             old_data = {}
            #             old_data['kitchen_title'] = post_data['kitchen_title']
            #             old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
            #             old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
            #             old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
            #             old_data['street_address_1'] = post_data['street_address_1']
            #             old_data['address_city'] = post_data['address_city'] or None
            #             old_data['address_postcode'] = post_data['address_postcode'] or None
            #             print("old data", old_data)
            #             request.session['_old_post'] = old_data 
            #             add_button_clicked = 0
            #             url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

            #             return HttpResponseRedirect(url)
            # address_city = request.POST.get('address_city') or None
            # print("address_city",address_city)
            # if address_city is None:
            #     kitchen_added_warning = 'Please enter city !'  
            #     messages.warning(request, kitchen_added_warning) 
            #     if '_old_post' in  request.session:
            #             del request.session['_old_post']
            #     old_data = {}
            #     old_data['kitchen_title'] = post_data['kitchen_title']
            #     old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
            #     old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
            #     old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
            #     old_data['street_address_1'] = post_data['street_address_1']
            #     old_data['address_city'] = post_data['address_city'] or None
            #     old_data['address_postcode'] = post_data['address_postcode'] or None
            #     print("old data", old_data)
            #     request.session['_old_post'] = old_data 
            #     add_button_clicked = 0
            #     url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

            #     return HttpResponseRedirect(url)
                
            #     # return redirect(request.META.get('HTTP_REFERER'))
            # else:
            #         if not address_city:
            #             kitchen_added_warning = 'Empty city not allowed !'  
            #             messages.warning(request, kitchen_added_warning) 
            #             if '_old_post' in  request.session:
            #                 del request.session['_old_post']
            #             old_data = {}
            #             old_data['kitchen_title'] = post_data['kitchen_title']
            #             old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
            #             old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
            #             old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
            #             old_data['street_address_1'] = post_data['street_address_1']
            #             old_data['address_city'] = post_data['address_city'] or None
            #             old_data['address_postcode'] = post_data['address_postcode'] or None
            #             print("old data", old_data)
            #             request.session['_old_post'] = old_data 
            #             add_button_clicked = 0
            #             url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

            #             return HttpResponseRedirect(url)
            # address_postcode = request.POST.get('address_postcode') or None
            # print("address_postcode",address_postcode)
            # if address_postcode is None:
            #     kitchen_added_warning = 'Please enter postal code !'  
            #     messages.warning(request, kitchen_added_warning) 
            #     if '_old_post' in  request.session:
            #             del request.session['_old_post']
            #     old_data = {}
            #     old_data['kitchen_title'] = post_data['kitchen_title']
            #     old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
            #     old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
            #     old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
            #     old_data['street_address_1'] = post_data['street_address_1']
            #     old_data['address_city'] = post_data['address_city'] or None
            #     old_data['address_postcode'] = post_data['address_postcode'] or None
            #     print("old data", old_data)
            #     request.session['_old_post'] = old_data 
            #     add_button_clicked = 0
            #     url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

            #     return HttpResponseRedirect(url)
                
            #     # return redirect(request.META.get('HTTP_REFERER'))
            # else:
            #         if not address_postcode:
            #             kitchen_added_warning = 'Empty postal code not allowed !'  
            #             messages.warning(request, kitchen_added_warning) 
            #             if '_old_post' in  request.session:
            #                 del request.session['_old_post']
            #             old_data = {}
            #             old_data['kitchen_title'] = post_data['kitchen_title']
            #             old_data['kitchen_owner_name'] = post_data['kitchen_owner_name']
            #             old_data['kitchen_owner_contact_number'] = post_data['kitchen_owner_contact_number'] or None
            #             old_data['kitchen_owner_email'] = post_data['kitchen_owner_email'] or None
            #             old_data['street_address_1'] = post_data['street_address_1']
            #             old_data['address_city'] = post_data['address_city'] or None
            #             old_data['address_postcode'] = post_data['address_postcode'] or None
            #             print("old data", old_data)
            #             request.session['_old_post'] = old_data 
            #             add_button_clicked = 0
            #             url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

            #             return HttpResponseRedirect(url)
                    
            # kitchen_images = request.FILES.getlist('kitchen_images') or None
            # print("kitchen_images",kitchen_images)

            

            kitchen_instance = Kitchen.objects.filter(pk=update_kitchen_pk).first()

            kitchen_instance.name =kitchen_name
            kitchen_instance.owner = owner_name
            kitchen_instance.contact = contact_number
            kitchen_instance.email = email 

            if lat is None:
                pass
            else: 

                try:
                    kitchen_admin = lat_long_nearest_admin(lat,long)
                except:
                    kitchen_admin = None

                kitchen_instance.kitchen_admin = kitchen_admin
                
                KitchenAddress_instance = kitchen_instance.kitchen_address_record
                KitchenAddress_instance.address_details = address_details
                KitchenAddress_instance.latitude = lat
                KitchenAddress_instance.longitude = long
                KitchenAddress_instance.save()

            kitchen_instance.save()

            # KitchenAddress_instance = KitchenAddress.objects.filter(Kitchen_id = update_kitchen_pk).first()

            # KitchenAddress_instance.address_line1 = street_address
            # KitchenAddress_instance.city =address_city
            # KitchenAddress_instance.postal_code = address_postcode
            # KitchenAddress_instance.save()


            # for image in kitchen_images:
            #     KitchenMedia.objects.create(Kitchen = kitchen_instance ,file=image)

            kitchen_added_success = 'Kitchen' + ' ' + kitchen_instance.name + ' ' + 'updated successfully !'  
            messages.success(request, kitchen_added_success)
            if '_old_post' in  request.session:
                del request.session['_old_post']    
            request.session['_old_post'] = None
            add_button_clicked = 0
            url = f'edit_kitchen_form/{update_kitchen_pk}/{add_button_clicked}'

            return HttpResponseRedirect(url)
            # return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'dashboard/permission_denied.html')
        


    
def KitchenSpecialitylist(request,id):  
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group) 

    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Kitchens'  in chk or request.user.is_superuser :
        
        kitchen_speciality = KitchenSpeciality.objects.filter(Kitchen=id).first()
        if not kitchen_speciality:
            ven = "Not Found"
            
        else: 
            items_ids = json.decoder.JSONDecoder().decode(kitchen_speciality.items)
            print("items_ids", items_ids)
            items = Menuitems.objects.filter(id__in=items_ids)
            print("selected items ",items)

            p = Paginator(Menuitems.objects.filter(id__in=items_ids).order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        print("ven",ven)
        context = {'ven':ven}
        print("checking alpha list",ven)
        return render(request, 'dashboard/Kitchens/kitchen_menu_list.html', context)
    
         
    else:
        return render(request, 'dashboard/permission_denied.html')
    


def KitchenOrderslist(request,id):  
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group) 

    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Kitchens'  in chk or request.user.is_superuser :
        
        kitchen_orders = Orders.objects.filter(kitchen_id=id).exists()
        if not kitchen_orders:
            ven = "Not Found"
            
        else: 
            p = Paginator(Orders.objects.filter(kitchen_id=id).order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        print("ven",ven)
        context = {'ven':ven}
        print("checking alpha list",ven)
        return render(request, 'dashboard/Kitchens/kitchen_orders_list.html', context)
    
         
    else:
        return render(request, 'dashboard/permission_denied.html')
    


def KitchenPreviousOrderslist(request,id):  
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group) 

    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'My Kitchen'  in chk or request.user.is_superuser :
        
        kitchen_orders = Orders.objects.filter(kitchen_id=id).exists()
        if not kitchen_orders:
            ven = "Not Found"
            
        else: 
            p = Paginator(Orders.objects.filter(kitchen_id=id).filter(status__in = ['Ready_for_pickup', 'Rider_on_the_way','Delivered']).order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        print("ven",ven)
        context = {'ven':ven}
        print("checking alpha list",ven)
        return render(request, 'dashboard/Kitchens/my_kitchen_previous_orders.html', context)
    
         
    else:
        return render(request, 'dashboard/permission_denied.html')
    
    

def  MyKitchenPreviousOrdersList(request):  
    chk = user_role(request.user)
    if len(chk) == 0:
      return redirect('login-dashboard')  
    elif len(chk) == 1 :
      return render(request, 'dashboard/permission_denied_updt.html')
    else: 
        if Kitchen.objects.filter(approved_owner_id=request.user.id).exists():
            all_order_status = Orderstatus.objects.filter(role = 'Kitchen').all()
            my_kitchen = Kitchen.objects.filter(approved_owner_id=request.user.id).first()
            if  not   Orders.objects.filter(kitchen_id=my_kitchen.id).exists() :
                context = {'ven': "Not Found"}
            else: 
                paginator = Paginator(Orders.objects.filter(kitchen_id=my_kitchen.id).filter(status__in = ['Ready_for_pickup', 'Rider_on_the_way','Delivered']).order_by('-id'), 15)
                page = request.GET.get('page')
                paginated_items = paginator.get_page(page)
                context= {'ven': paginated_items,'my_kitchen':my_kitchen,'all_order_status':all_order_status}
             
        else:
            return render(request, 'dashboard/permission_denied_updt.html')
      
    return render(request, 'dashboard/Kitchens/my_kitchen_orders.html', context)
