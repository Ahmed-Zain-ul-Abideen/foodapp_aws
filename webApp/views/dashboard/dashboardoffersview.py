from django.shortcuts import render,redirect, HttpResponseRedirect
from webApp.models import *
from django.contrib import messages
from django.core.paginator import Paginator
from geopy.geocoders import Nominatim
from django.http import JsonResponse
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth import logout
from webApp.templatetags.webApp_extras import user_role
from webApp.views.Regex_setting import cleanhtml
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
channel_layer = get_channel_layer()

from webApp.views.expo_notif_view import send_salient_data_message



def AddOfferForm(request,add_button_clicked=None):
    
    re_render = False
    all_items = Menuitems.objects.filter(daily_deals = True).all()
    all_addons = Alladdson.objects.all()

    context= {'re_render':re_render,
                'all_items':all_items,
                'all_addons':all_addons}
    return render(request, 'dashboard/Offers/add_offer_form.html', context)
    


def AddOffer(request):
    

    if request.method == 'POST': 
        
        offer_name = request.POST.get('offer_name') or None
        print("offer_name",offer_name)

        if offer_name is None:
            item_added_warning = 'Please enter name!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        

        offer_price = request.POST.get('offer_price') or None
        print("offer_price",offer_price)

        if offer_price is None:
            item_added_warning = 'Please enter price!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        
        offer_image = request.FILES.get('offer_image') or None

        
           
        if offer_image is not  None:  
            if offer_image.content_type.startswith('image'):
                pass
            else:
                item_added_warning = 'Please image file !'  
                messages.warning(request, item_added_warning)
                return redirect(request.META.get('HTTP_REFERER')) 
        else: 
            
            item_added_warning = 'Please upload image!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER')) 
        


        offer_items = request.POST.getlist('selected_item_cat_dropdown') or None
        print("selected items",offer_items)
        if offer_items is None:
            topic_added_warning = 'Please select at least 1 item for offer!'  
            messages.warning(request, topic_added_warning)    
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            if not len(offer_items):
                topic_added_warning = 'Please select at least 1 item for offer!'  
                messages.warning(request, topic_added_warning)   
                return redirect(request.META.get('HTTP_REFERER'))
            

        
        offer_addons = request.POST.getlist('selected_item_cat_dropdown_addons') or None
        print("selected addons",offer_addons)
        
            
        offer_description = request.POST.get('offer_description') or None
        print("offer_description",offer_description)

        if offer_description is None:
            item_added_warning = 'Please enter description!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        

        if offer_description:
            offer_description = cleanhtml(offer_description)

        offer_instance = Deals.objects.create(title = offer_name,price = offer_price, file = offer_image, description=offer_description)
        offer_instance.save()
        
        #  linking items 
        menu_items = Menuitems.objects.filter(id__in=offer_items)

        for menu_item in menu_items:
            
            menu_item.deal.add(offer_instance)
            menu_item.save()

        #  linking addon
        if offer_addons:
            add_ons = Alladdson.objects.filter(id__in =offer_addons)

            for add_on in add_ons:
                
                add_on.deal.add(offer_instance)
                add_on.save()

        else:
            offer_instance.deal_addson_records.clear()


        # Send Data message
        list_of_fcm = list(Orders.objects.values_list('order_fcm', flat=True).distinct())
        print("list_of_fcm", list_of_fcm)

        for token in list_of_fcm:
            try:
                extra = {"newData": "3"}
                send_salient_data_message(token, extra)
            except Exception as e:
                print("Error:", e)
        # End Send Data message


        item_added_success = 'Offer' + ' ' + offer_instance.title + ' ' + 'added successfully !'  
        messages.success(request, item_added_success)
        
            
        return redirect(request.META.get('HTTP_REFERER'))
    
    return render(request, 'dashboard/Offers/add_offer_form.html')






def EditOfferForm(request,id,add_button_clicked=None):


    all_addons = Alladdson.objects.all()
    all_items = Menuitems.objects.filter(daily_deals = True).all()
    re_render = False
    offer_instance = Deals.objects.filter(pk=id).first()

    offer_items = list(Menuitems.objects.filter(deal=offer_instance).values_list('id', flat=True))
    offer_addons = list(Alladdson.objects.filter(deal=offer_instance).values_list('id', flat=True))

    print("list of offer list ",offer_items)

    context= {'re_render':re_render,
                'offer_instance':offer_instance,
                'offer_items':offer_items,
                'all_items':all_items,
                'all_addons':all_addons,
                'offer_addons':offer_addons
                
                }
    return render(request, 'dashboard/Offers/edit_offer_form.html', context)

    

def EditOffer(request):
    
    
    if request.method == 'POST': 
        

        update_offer_pk = request.POST.get('update_offer_pk') or None
        print("update_offer_pk",update_offer_pk)

        offer_name = request.POST.get('offer_name') or None
        print("offer_name",offer_name)

        if offer_name is None:
            item_added_warning = 'Please enter name!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        

        offer_price = request.POST.get('offer_price') or None
        print("offer_price",offer_price)

        if offer_price is None:
            item_added_warning = 'Please enter price!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        

        offer_image = request.FILES.get('offer_image') or None
        print("offer_image",offer_image)


        if offer_image:
            file_extension = offer_image.name.split('.')[-1].lower()
            print("file extention", file_extension)
        
            if file_extension in ['png', 'jpg', 'jpeg', 'webp']:
                pass
            else:
                name_added_warning = 'Uplaod image file Only !'  
                messages.warning(request, name_added_warning)   
                return redirect(request.META.get('HTTP_REFERER'))

        
        


        offer_items = request.POST.getlist('selected_item_cat_dropdown') or None
        print("selected items",offer_items)
        if offer_items is None:
            topic_added_warning = 'Please select at least 1 item for offer!'  
            messages.warning(request, topic_added_warning)    
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            if not len(offer_items):
                topic_added_warning = 'Please select at least 1 item for offer!'  
                messages.warning(request, topic_added_warning)   
                return redirect(request.META.get('HTTP_REFERER'))
            
        offer_addons = request.POST.getlist('selected_item_cat_dropdown_addons') or None
        print("selected addons",offer_addons)
        

    
        offer_description = request.POST.get('offer_description') or None
        print("offer_description",offer_description)

        if offer_description is None:
            item_added_warning = 'Please enter description!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        

        if offer_description:
            offer_description = cleanhtml(offer_description)
        
        

        offer_instance = Deals.objects.filter(pk=update_offer_pk).first()

        offer_instance.title = offer_name
        offer_instance.price = offer_price
        offer_instance.description = offer_description

        if offer_image:
            offer_instance.file = offer_image

        offer_instance.save()

        # linking items
        if offer_items:
            menu_items = Menuitems.objects.filter(id__in=offer_items)

            for menu_item in menu_items:
                
                menu_item.deal.add(offer_instance)
                menu_item.save()
        # else:
        #     offer_instance.deal_items.clear()



        #  linking addon
        if offer_addons:
            add_ons = Alladdson.objects.filter(id__in =offer_addons)

            for add_on in add_ons:
                
                add_on.deal.add(offer_instance)
                add_on.save()
        
        else:
            offer_instance.deal_addson_records.clear()



        # Send Data message
        list_of_fcm = list(Orders.objects.values_list('order_fcm', flat=True).distinct())
        print("list_of_fcm", list_of_fcm)

        for token in list_of_fcm:
            try:
                extra = {"newData": "3"}
                send_salient_data_message(token, extra)
            except Exception as e:
                print("Error:", e)
        # End Send Data message

        item_added_success = 'Offer' + ' ' + offer_instance.title + ' ' + 'updated successfully !'  
        messages.success(request, item_added_success)
        
            
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))



def Offerlist(request):  
    

    all_offers = Deals.objects.exists()
    if not all_offers:
        ven = "Not Found"
        
        
    else: 
        p = Paginator(Deals.objects.order_by('-id'),15)
        page = request.GET.get('page')
        ven = p.get_page(page) 
        
    context = {'ven':ven }
    return render(request, 'dashboard/Offers/index.html', context)



def DeleteOffer(request,id=None):
    
    
    print("here for deleteing offer record")
    offer_id = request.GET.get("offer_id")    
    print("offer_id", offer_id)
    offer_instance = Deals.objects.filter(id=offer_id).first()
    offer_name = offer_instance.title

    offer_instance.delete() 
    print("offer record deleted Successfully!")
    data = {'item_name':offer_name}
    return JsonResponse(data)
    


# Delete offer Image
def DeleteOfferImage(request,id):
    offer_id = request.GET.get("offer_id") 
    print("offer_id",offer_id)
    profile_pic_flag = True
    offer_instance = Deals.objects.filter(pk=offer_id).first()
    if offer_instance.file is None:
        profile_pic_flag = False
    else:
        if not offer_instance.file:
            profile_pic_flag = False
        else:
            offer_instance.file.delete(save=False)
            offer_instance.save() 
    data = {'user_name':offer_instance.title,'profile_pic_flag':profile_pic_flag}
    return JsonResponse(data)
    
    
