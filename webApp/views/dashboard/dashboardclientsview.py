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



def AddTestimonialForm(request,add_button_clicked=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if request.user.is_superuser:
        re_render = False

        
        context= {'re_render':re_render}
        return render(request, 'dashboard/Web_Clients/add_testimonial_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')
    


def AddTestimonial(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if request.user.is_superuser :

        
        client_name = request.POST.get('client_name') or None
        print("client_name",client_name)

        if client_name is None:
            user_added_warning = 'Please enter name!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))

        
        client_review = request.POST.get('client_review') or None
        print("client_review",client_review)

        if client_review is None:
            user_added_warning = 'Please enter review!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        if client_review:
                client_review = cleanhtml(client_review)


        client_image = request.FILES.get('client_image') or None

        print("client_image",client_image)

        
           
        if client_image is not  None:  
            
            file_extension = client_image.name.split('.')[-1].lower()
            print("file extention", file_extension)
        
            if file_extension in ['png', 'jpg', 'jpeg', 'webp']:
                pass
            else:
                name_added_warning = 'Uplaod image file Only !'  
                messages.warning(request, name_added_warning)   
                return redirect(request.META.get('HTTP_REFERER'))
        
        client_base_instance = Clients.objects.first()
        if client_base_instance:
            OurClients.objects.create(name = client_name, review=client_review, avatar = client_image,client = client_base_instance)
        
        else:
                name_added_warning = 'Add base section section first!'  
                messages.warning(request, name_added_warning)   
                return redirect(request.META.get('HTTP_REFERER'))

      

        item_added_success = 'Testimonial added successfully !'  
        messages.success(request, item_added_success)
        
            
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'dashboard/permission_denied.html')
    





def EditTestimonialForm(request,id,add_button_clicked=None):
    
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if request.user.is_superuser:
        re_render = False
        testimonial_instance = OurClients.objects.filter(pk=id).first()

        context= {'re_render':re_render,
                  'testimonial_instance':testimonial_instance,
                  
                  }
        return render(request, 'dashboard/Web_Clients/edit_testimonial_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')
    

def EditTestinomial(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if request.user.is_superuser :

        update_testimonial_pk = request.POST.get('update_testimonial_pk') or None
        print("update_testimonial_pk",update_testimonial_pk)

        client_name = request.POST.get('client_name') or None
        print("client_name",client_name)

        if client_name is None:
            user_added_warning = 'Please enter name!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))

        
        client_review = request.POST.get('client_review') or None
        print("client_review",client_review)

        if client_review is None:
            user_added_warning = 'Please enter review!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        if client_review:
                client_review = cleanhtml(client_review)


        client_image = request.FILES.get('client_image') or None

        print("client_image",client_image)

        
           
        if client_image is not  None:  
            
            file_extension = client_image.name.split('.')[-1].lower()
            print("file extention", file_extension)
        
            if file_extension in ['png', 'jpg', 'jpeg', 'webp']:
                pass
            else:
                name_added_warning = 'Uplaod image file Only !'  
                messages.warning(request, name_added_warning)   
                return redirect(request.META.get('HTTP_REFERER'))
        
        client_base_instance = Clients.objects.first()
        if client_base_instance:
            testimonial_instance = OurClients.objects.filter(id = update_testimonial_pk).first()
            testimonial_instance.name = client_name
            testimonial_instance.review = client_review
            if client_image:
                testimonial_instance.avatar = client_image
            testimonial_instance.client= client_base_instance

            testimonial_instance.save()
        
        else:
                name_added_warning = 'Add base section first!'  
                messages.warning(request, name_added_warning)   
                return redirect(request.META.get('HTTP_REFERER'))

      

        item_added_success = 'Testimonial updated successfully !'  
        messages.success(request, item_added_success)
        
            
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'dashboard/permission_denied.html')
    





def Testimoniallist(request):  
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if request.user.is_superuser:

        all_items = OurClients.objects.exists()
        if not all_items:
            ven = "Not Found"
            
            
        else: 
            p = Paginator(OurClients.objects.order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
            
        context = {'ven':ven }
        return render(request, 'dashboard/Web_Clients/index.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')
    


def DeleteTestimonial(request,id=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if request.user.is_superuser:
    
        print("here for deleteing service record")
        testimonial_id = request.GET.get("testimonial_id")    
        print("testimonial_id", testimonial_id)
        testimonial_instance = OurClients.objects.filter(id=testimonial_id).first()
        testimonial_name = testimonial_instance.name

        testimonial_instance.delete() 
        print("record testimonial deleted Successfully!")
        data = {'item_name':testimonial_name}
        return JsonResponse(data)
    else:
        return render(request, 'dashboard/permission_denied.html')
    



def ClientSectionForm(request):
    if Clients.objects.exists():
        re_render = False
        our_client_section_instance = Clients.objects.first()
        print(our_client_section_instance)

        context= {'re_render':re_render,'our_client_section_instance':our_client_section_instance}
        

    else:
        new_record = True
        context= {'new_record':new_record}


    return render(request, 'dashboard/Web_Clients/client_section_form.html', context)



def EditClientSectionForm(request):
    if request.method == 'POST':

        client_section_title = request.POST.get('client_section_title') or None
        print("client_section_title",client_section_title)

        if client_section_title is None:
            user_added_warning = 'Please enter client section title!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        client_section_description = request.POST.get('client_section_description') or None
        print("client_section_description",client_section_description)

        if client_section_description is None:
            user_added_warning = 'Please enter client section description!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))

        
        if Clients.objects.exists():

            client_instance = Clients.objects.first()
            client_instance.title = client_section_title
            client_instance.description = client_section_description

            client_instance.save()
        else:
            Clients.objects.create(title = client_section_title, description = client_section_description)


        group_added_success = 'Client section updated successfully !'  
        messages.success(request, group_added_success)
            
        return redirect(request.META.get('HTTP_REFERER'))

