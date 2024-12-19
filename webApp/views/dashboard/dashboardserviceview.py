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
from webApp.views.Regex_setting import cleanhtml



def AddServiceForm(request,add_button_clicked=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if request.user.is_superuser:
        re_render = False

        
        context= {'re_render':re_render}
        return render(request, 'dashboard/Web_Services/add_service_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')
    


def AddService(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if request.user.is_superuser :

        
        service_title = request.POST.get('service_title') or None
        print("service_title",service_title)

        if service_title is None:
            user_added_warning = 'Please enter service title!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))

        
        service_description = request.POST.get('service_description') or None
        print("service_description",service_description)

        if service_description is None:
            user_added_warning = 'Please enter service description!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        if service_description:
                service_description = cleanhtml(service_description)


        service_image = request.FILES.get('service_image') or None

        print("service_image",service_image)

        
           
        if service_image is not  None:  
            
            file_extension = service_image.name.split('.')[-1].lower()
            print("file extention", file_extension)
        
            if file_extension in ['png', 'jpg', 'jpeg', 'webp']:
                pass
            else:
                name_added_warning = 'Uplaod image file Only !'  
                messages.warning(request, name_added_warning)   
                return redirect(request.META.get('HTTP_REFERER'))
        
        service_title_instance = OurServicesSection.objects.first()
        if service_title_instance:
            OurServices.objects.create(title = service_title, description=service_description, image = service_image,service = service_title_instance)
        
        else:
                name_added_warning = 'Add service section first!'  
                messages.warning(request, name_added_warning)   
                return redirect(request.META.get('HTTP_REFERER'))

      

        item_added_success = 'Service added successfully !'  
        messages.success(request, item_added_success)
        
            
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'dashboard/permission_denied.html')
    





def EditServiceForm(request,id,add_button_clicked=None):
    
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if request.user.is_superuser:
        re_render = False
        service_instance = OurServices.objects.filter(pk=id).first()

        context= {'re_render':re_render,
                  'service_instance':service_instance,
                  
                  }
        return render(request, 'dashboard/Web_Services/edit_service_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')
    

def EditService(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if request.user.is_superuser :

        update_service_pk = request.POST.get('update_service_pk') or None
        print("update_service_pk",update_service_pk)

        service_title = request.POST.get('service_title') or None
        print("service_title",service_title)

        if service_title is None:
            user_added_warning = 'Please enter service title!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))

        
        service_description = request.POST.get('service_description') or None
        print("service_description",service_description)

        if service_description is None:
            user_added_warning = 'Please enter service description!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        if service_description:
                service_description = cleanhtml(service_description)


        service_image = request.FILES.get('service_image') or None

        print("service_image",service_image)

        
           
        if service_image is not  None:  
            
            file_extension = service_image.name.split('.')[-1].lower()
            print("file extention", file_extension)
        
            if file_extension in ['png', 'jpg', 'jpeg', 'webp']:
                pass
            else:
                name_added_warning = 'Uplaod image file Only !'  
                messages.warning(request, name_added_warning)   
                return redirect(request.META.get('HTTP_REFERER'))
        
        service_title_instance = OurServicesSection.objects.first()
        if service_title_instance:
            service_instance = OurServices.objects.filter(id = update_service_pk).first()
            service_instance.title = service_title
            service_instance.description = service_description
            if service_image:
                service_instance.image = service_image
            service_instance.service= service_title_instance

            service_instance.save()
        
        else:
                name_added_warning = 'Add service section first!'  
                messages.warning(request, name_added_warning)   
                return redirect(request.META.get('HTTP_REFERER'))

      

        item_added_success = 'Service updated successfully !'  
        messages.success(request, item_added_success)
        
            
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'dashboard/permission_denied.html')
    





def Servicelist(request):  
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if request.user.is_superuser:

        all_items = OurServices.objects.exists()
        if not all_items:
            ven = "Not Found"
            
            
        else: 
            p = Paginator(OurServices.objects.order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
            
        context = {'ven':ven }
        return render(request, 'dashboard/Web_Services/index.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')
    


def DeleteService(request,id=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if request.user.is_superuser:
    
        print("here for deleteing service record")
        service_id = request.GET.get("service_id")    
        print("service_id", service_id)
        service_instance = OurServices.objects.filter(id=service_id).first()
        service_name = service_instance.title

        service_instance.delete() 
        print("record service deleted Successfully!")
        data = {'item_name':service_name}
        return JsonResponse(data)
    else:
        return render(request, 'dashboard/permission_denied.html')