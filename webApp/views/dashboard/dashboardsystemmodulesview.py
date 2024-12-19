from django.shortcuts import render,redirect, HttpResponseRedirect
from webApp.models import *
from django.contrib import messages
from django.core.paginator import Paginator
from geopy.geocoders import Nominatim
from django.http import JsonResponse
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth import logout
from webApp.templatetags.webApp_extras import user_role




def SystemModulesList(request):  
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if request.user.is_superuser:
     
    
        all_systemmodules = SystemModules.objects.exists()
        if not all_systemmodules:
            ven = "Not Found"
            
        else: 
            p = Paginator(SystemModules.objects.all().order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        context = {'ven':ven}
        return render(request, 'dashboard/System_Modules/index.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')
    

def AddSystemModuleForm(request,add_button_clicked=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if request.user.is_superuser:
        re_render = False
        module = SystemModules.objects.all()

        context= {'re_render':re_render,'module':module}
        return render(request, 'dashboard/System_Modules/add_systemmodule_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')
    


def EditSystemModuleForm(request,id,add_button_clicked=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if request.user.is_superuser:
        re_render = False
        module = SystemModules.objects.filter(id = id).first()


        context= {'re_render':re_render,'module':module}
        return render(request, 'dashboard/System_Modules/edit_systemmodule_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')
    
def AddSystemModule(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if request.user.is_superuser:
        if request.method == 'POST':
            
            system_module_title = request.POST.get('system_module_title') or None
            print("system_module_title",system_module_title)


            if system_module_title is None:
                user_added_warning = 'Please enter name!'  
                messages.warning(request, user_added_warning)
                return redirect(request.META.get('HTTP_REFERER'))


            system_module_instance = SystemModules.objects.create(module = system_module_title)
            system_module_instance.save()


            group_added_success = 'System Module' + ' ' + system_module_instance.module + ' ' + 'added successfully !'  
            messages.success(request, group_added_success)
            
                
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'dashboard/permission_denied.html')





def EditSystemModule(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if request.user.is_superuser:
        
        system_module_pk = request.POST.get('system_module_pk') or None
        print("system_module_pk",system_module_pk)

        system_module_title = request.POST.get('system_module_title') or None
        print("system_module_title",system_module_title)



        if system_module_title is None:
            user_added_warning = 'Please enter name!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))

        system_module_instance = SystemModules.objects.filter(pk = system_module_pk).first()

        system_module_instance.module = system_module_title
        system_module_instance.save()


        group_added_success = 'System Module' + ' ' + system_module_instance.module + ' ' + 'updated successfully !'  
        messages.success(request, group_added_success)
            
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'dashboard/permission_denied.html')
    




def DeleteSystemModule(request,id=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)

    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if request.user.is_superuser:
    
        print("here for deleteing systemmodule record")
        system_module_id = request.GET.get("module_id")    
        print("system_module_id", system_module_id)
        system_module_instance = SystemModules.objects.filter(id=system_module_id).first()
        system_module_name = system_module_instance.module


        LinkGroupModule.objects.filter(module=system_module_name).delete()


        system_module_instance.delete() 
        print("record deleted Successfully!")
        data = {'system_module_name':system_module_name}
        return JsonResponse(data)
    else:
        return render(request, 'dashboard/permission_denied.html')
    


def FoodappSetting(request):
    if FoodappSettings.objects.exists():
        re_render = False
        setting_instance = FoodappSettings.objects.first()
        print(setting_instance)

        context= {'re_render':re_render,'setting_instance':setting_instance}
        

    else:
        new_record = True
        context= {'new_record':new_record}


    return render(request, 'dashboard/System_Modules/foodapp_setting.html', context)

    

from webApp.views.Regex_setting import cleanhtml


def EditFoodappSetting(request):
    if request.method == 'POST':

        foodapp_contact = request.POST.get('foodapp_contact') or None
        print("foodapp_contact",foodapp_contact)

        if foodapp_contact is None:
            user_added_warning = 'Please enter 2 contact number!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))

        order_radius = request.POST.get('order_radius') or None
        print("order_radius",order_radius)

        if order_radius is None:
            user_added_warning = 'Please enter order radius!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        term_conditions = request.POST.get('term_conditions') or None
        print("term_conditions",term_conditions)

        if term_conditions is None:
            user_added_warning = 'Please enter Term & Conditions!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))

        kithcen_perc = request.POST.get('kithcen_perc') or None
        if kithcen_perc is None:
            user_added_warning = 'Please enter kitchen percentage per order!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        if term_conditions:
                term_conditions = cleanhtml(term_conditions)
        if FoodappSettings.objects.exists():

            setting_instance = FoodappSettings.objects.first()
            setting_instance.contact = foodapp_contact
            setting_instance.orders_radius = order_radius
            setting_instance.terms_and_c = term_conditions
            setting_instance.Kitchen_share_percent = kithcen_perc

            setting_instance.save()
        else:
            FoodappSettings.objects.create(Kitchen_share_percent=kithcen_perc,contact = foodapp_contact, orders_radius= order_radius, terms_and_c = term_conditions)


        group_added_success = 'FoodApp Setting updated successfully !'  
        messages.success(request, group_added_success)
            
        return redirect(request.META.get('HTTP_REFERER'))



def WebDynamicContentForm(request):
    if WebsiteDynamic.objects.exists():
        re_render = False
        web_dynamic_instance = WebsiteDynamic.objects.first()
        print(web_dynamic_instance)

        context= {'re_render':re_render,'web_dynamic_instance':web_dynamic_instance}
        

    else:
        new_record = True
        context= {'new_record':new_record}


    return render(request, 'dashboard/System_Modules/web_dynamic_content.html', context)

def EditWebDynamicContent(request):
    if request.method == 'POST':

        hero_section_title = request.POST.get('hero_section_title') or None
        print("hero_section_title",hero_section_title)

        if hero_section_title is None:
            user_added_warning = 'Please enter hero section title!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))

        
        hero_section_description = request.POST.get('hero_section_description') or None
        print("hero_section_description",hero_section_description)

        if hero_section_description is None:
            user_added_warning = 'Please enter hero section description!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        if hero_section_description:
                hero_section_description = cleanhtml(hero_section_description)


        hero_section_image = request.FILES.get('hero_section_image') or None

        print("hero_section_image",hero_section_image)

        
           
        if hero_section_image is not  None:  
            
            file_extension = hero_section_image.name.split('.')[-1].lower()
            print("file extention", file_extension)
        
            if file_extension in ['png', 'jpg', 'jpeg', 'webp']:
                pass
            else:
                name_added_warning = 'Uplaod image file Only !'  
                messages.warning(request, name_added_warning)   
                return redirect(request.META.get('HTTP_REFERER'))
        
        
        # About Section
        about_section_title = request.POST.get('about_section_title') or None
        print("about_section_title",about_section_title)

        if about_section_title is None:
            user_added_warning = 'Please enter about section title!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))

        
        about_section_description = request.POST.get('about_section_description') or None
        print("about_section_description",about_section_description)

        if about_section_description is None:
            user_added_warning = 'Please enter about section description!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        if about_section_description:
                about_section_description = cleanhtml(about_section_description)


        about_section_image = request.FILES.get('about_section_image') or None

        
           
        if about_section_image is not  None:  
            file_extension = about_section_image.name.split('.')[-1].lower()
            print("file extention", file_extension)
        
            if file_extension in ['png', 'jpg', 'jpeg', 'webp']:
                pass
            else:
                name_added_warning = 'Uplaod image file Only !'  
                messages.warning(request, name_added_warning)   
                return redirect(request.META.get('HTTP_REFERER')) 
        
        

        # Daily Section
        daily_section_title = request.POST.get('daily_section_title') or None
        print("daily_section_title",daily_section_title)

        if daily_section_title is None:
            user_added_warning = 'Please enter daily section title!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))

        
        daily_section_description = request.POST.get('daily_section_description') or None
        print("daily_section_description",daily_section_description)

        if daily_section_description is None:
            user_added_warning = 'Please enter daily section description!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        if daily_section_description:
                daily_section_description = cleanhtml(daily_section_description)


        # Menu Section
        menu_section_title = request.POST.get('menu_section_title') or None
        print("menu_section_title",menu_section_title)

        if menu_section_title is None:
            user_added_warning = 'Please enter menu section title!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))

        
        menu_section_description = request.POST.get('menu_section_description') or None
        print("menu_section_description",menu_section_description)

        if menu_section_description is None:
            user_added_warning = 'Please enter menu section description!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        if menu_section_description:
                menu_section_description = cleanhtml(menu_section_description)
        
        if WebsiteDynamic.objects.exists():

            web_dynamic_instance = WebsiteDynamic.objects.first()
            web_dynamic_instance.Hero_section_title = hero_section_title
            web_dynamic_instance.Hero_section_description = hero_section_description
            if hero_section_image:
                web_dynamic_instance.Hero_section_image = hero_section_image
            
            # about section
            web_dynamic_instance.about_section_title = about_section_title
            web_dynamic_instance.about_section_description = about_section_description
            if about_section_image:
                web_dynamic_instance.about_section_image = about_section_image
            # daily section
            web_dynamic_instance.daily_section_title = daily_section_title
            web_dynamic_instance.daily_section_description = daily_section_description
            # menu section
            web_dynamic_instance.menus_section_title = menu_section_title
            web_dynamic_instance.menus_section_description = menu_section_description

            web_dynamic_instance.save()
        else:
            WebsiteDynamic.objects.create(Hero_section_title = hero_section_title, Hero_section_description = hero_section_description,
                                          Hero_section_image = hero_section_image, about_section_title=about_section_title,
                                          about_section_description=about_section_description,about_section_image=about_section_image,
                                          daily_section_title=daily_section_title,daily_section_description=daily_section_description,
                                          menus_section_title=menu_section_title,menus_section_description=menu_section_description)


        group_added_success = 'Web Content updated successfully !'  
        messages.success(request, group_added_success)
            
        return redirect(request.META.get('HTTP_REFERER'))
    

def ServicesSectionForm(request):
    if OurServicesSection.objects.exists():
        re_render = False
        our_service_section_instance = OurServicesSection.objects.first()
        print(our_service_section_instance)

        context= {'re_render':re_render,'our_service_section_instance':our_service_section_instance}
        

    else:
        new_record = True
        context= {'new_record':new_record}


    return render(request, 'dashboard/System_Modules/services_title_form.html', context)



def EditServicesSectionForm(request):
    if request.method == 'POST':

        service_section_title = request.POST.get('service_section_title') or None
        print("service_section_title",service_section_title)

        if service_section_title is None:
            user_added_warning = 'Please services title!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))

        
        if OurServicesSection.objects.exists():

            setting_instance = OurServicesSection.objects.first()
            setting_instance.title = service_section_title
            

            setting_instance.save()
        else:
            OurServicesSection.objects.create(title = service_section_title)


        group_added_success = 'Service title updated successfully !'  
        messages.success(request, group_added_success)
            
        return redirect(request.META.get('HTTP_REFERER'))

