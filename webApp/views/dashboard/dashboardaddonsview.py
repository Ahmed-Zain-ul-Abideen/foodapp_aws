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




def AddAddonsForm(request,add_button_clicked=None):
    
    re_render = False
    context= {'re_render':re_render}
    return render(request, 'dashboard/Add_Ons/add_addons_form.html', context)


def AddAddons(request):
    

    if request.method == 'POST': 
        
        addon_name = request.POST.get('addon_name') or None
        print("addon_name",addon_name)

        if addon_name is None:
            item_added_warning = 'Please enter name!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        

        addon_price = request.POST.get('addon_price') or None
        print("addon_price",addon_price)

        if addon_price is None:
            item_added_warning = 'Please enter price!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        
        addon_image = request.FILES.get('addon_image') or None

        
           
        if addon_image is not  None:  
            if addon_image.content_type.startswith('image'):
                pass
            else:
                item_added_warning = 'Please image file !'  
                messages.warning(request, item_added_warning)
                return redirect(request.META.get('HTTP_REFERER')) 
        else: 
            
            item_added_warning = 'Please upload image!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER')) 
        
        addon_description = request.POST.get('addon_description') or None
        print("addon_description",addon_description)

        if addon_description is None:
            item_added_warning = 'Please enter description!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        

        if addon_description:
            addon_description = cleanhtml(addon_description)

        addon_instance = Alladdson.objects.create(title = addon_name,price = addon_price, image = addon_image, description=addon_description)
        addon_instance.save()
        
        



        item_added_success = 'AddOn' + ' ' + addon_instance.title + ' ' + 'added successfully !'  
        messages.success(request, item_added_success)
        
            
        return redirect(request.META.get('HTTP_REFERER'))
    
    return render(request, 'dashboard/Add_Ons/add_addons_form.html')




def EditAddonsForm(request,id,add_button_clicked=None):
    
    re_render = False
    addon_instance = Alladdson.objects.filter(pk=id).first()


    context= {'re_render':re_render,
                'addon_instance':addon_instance
                }
    
    return render(request, 'dashboard/Add_Ons/edit_addons_form.html', context)





def EditAddons(request):
    
    
    if request.method == 'POST': 
        

        update_addon_pk = request.POST.get('update_addon_pk') or None
        print("update_addon_pk",update_addon_pk)

        addon_name = request.POST.get('addon_name') or None
        print("addon_name",addon_name)

        if addon_name is None:
            item_added_warning = 'Please enter name!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        

        addon_price = request.POST.get('addon_price') or None
        print("addon_price",addon_price)

        if addon_price is None:
            item_added_warning = 'Please enter price!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        

        addon_image = request.FILES.get('addon_image') or None
        print("addon_image",addon_image)


        if addon_image:
            file_extension = addon_image.name.split('.')[-1].lower()
            print("file extention", file_extension)
        
            if file_extension in ['png', 'jpg', 'jpeg', 'webp']:
                pass
            else:
                name_added_warning = 'Uplaod image file Only !'  
                messages.warning(request, name_added_warning)   
                return redirect(request.META.get('HTTP_REFERER'))
      
    
        addon_description = request.POST.get('addon_description') or None
        print("addon_description",addon_description)

        if addon_description is None:
            item_added_warning = 'Please enter description!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        

        if addon_description:
            addon_description = cleanhtml(addon_description)
        
        

        addon_instance = Alladdson.objects.filter(pk=update_addon_pk).first()

        addon_instance.title = addon_name
        addon_instance.price = addon_price
        addon_instance.description = addon_description

        if addon_instance:
            addon_instance.image = addon_image

        addon_instance.save()


        item_added_success = 'AddOn' + ' ' + addon_instance.title + ' ' + 'updated successfully !'  
        messages.success(request, item_added_success)
        
            
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))




def Addonslist(request):  
    

    all_addons = Alladdson.objects.exists()
    if not all_addons:
        ven = "Not Found"
        
        
    else: 
        p = Paginator(Alladdson.objects.order_by('-id'),15)
        page = request.GET.get('page')
        ven = p.get_page(page) 
        
    context = {'ven':ven }
    return render(request, 'dashboard/Add_Ons/index.html', context)



def DeleteAddons(request,id=None):
    
    
    print("here for deleteing addon record")
    addon_id = request.GET.get("addon_id")    
    print("addon_id", addon_id)
    addon_instance = Alladdson.objects.filter(id=addon_id).first()
    addon_name = addon_instance.title

    addon_instance.delete() 
    print("addon record deleted Successfully!")
    data = {'item_name':addon_name}
    return JsonResponse(data)




# Delete addon Image
def DeleteAddonsImage(request,id):
    addon_id = request.GET.get("addon_id") 
    print("addon_id",addon_id)
    profile_pic_flag = True
    addon_instance = Alladdson.objects.filter(pk=addon_id).first()
    if addon_instance.image is None:
        profile_pic_flag = False
    else:
        if not addon_instance.image:
            profile_pic_flag = False
        else:
            addon_instance.image.delete(save=False)
            addon_instance.save() 
    data = {'user_name':addon_instance.title,'profile_pic_flag':profile_pic_flag}
    return JsonResponse(data)