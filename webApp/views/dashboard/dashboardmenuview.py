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


def MenuCategorieslist(request):  
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'Menus'  in chk or request.user.is_superuser:
    
        all_menus_categories = MenuCategory.objects.exists()
        if not all_menus_categories:
            ven = "Not Found"
            
        else: 
            p = Paginator(MenuCategory.objects.all().order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        context = {'ven':ven}
        return render(request, 'dashboard/Menus/menu_categories_list.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')
    




def Menulist(request,id):  
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'Menus'  in chk or request.user.is_superuser:
        menu_cat_id = id
        print('menu_cat_id',menu_cat_id)
        menu_category_instance = MenuCategory.objects.filter(id =id ).first()
        all_menus = Menu.objects.filter(category_id = id).exists()
        if not all_menus:
            ven = "Not Found"
            
            
        else: 
            p = Paginator(Menu.objects.filter(category_id = id).order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
            
        context = {'ven':ven,
                   'menu_category_instance':menu_category_instance
                   }
        return render(request, 'dashboard/Menus/menus_list.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')




def AddMenuForm(request,add_button_clicked=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'Menus'  in chk or request.user.is_superuser:
        re_render = False
        menu_categories = MenuCategory.objects.all()
        all_addons = Alladdson.objects.all()


        
        context= {'re_render':re_render,'menu_categories':menu_categories,
                  'all_addons':all_addons}
        return render(request, 'dashboard/Menus/add_menu_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')





def AddMenu(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'Menus'  in chk or request.user.is_superuser :
        if request.method == 'POST':
            # re_render = False
            # post_data = request.POST
            # selcted_menu_flag = True

            selected_menu_cat = request.POST.get('selected_menu_cat_dropdown') or None
            print("selected_menu_cat",selected_menu_cat)

            # if selected_menu_cat is None:
            #     selcted_menu_flag = False
            # else:
            #     if not len(selected_menu_cat):
            #         selcted_menu_flag = False


            

            menu_name = request.POST.get('menu_name') or None
            print("menu_name",menu_name)

            if menu_name is None:
                user_added_warning = 'Please enter name!'  
                messages.warning(request, user_added_warning)
                return redirect(request.META.get('HTTP_REFERER'))

            menu_price = request.POST.get('menu_price') or None
            print("menu_price",menu_price)

            if menu_price is None:
                user_added_warning = 'Please enter price!'  
                messages.warning(request, user_added_warning)
                return redirect(request.META.get('HTTP_REFERER'))
            
            discounted_price = request.POST.get('discounted_price') or None
            print("discounted_price",discounted_price)

            if selected_menu_cat is None:
                user_added_warning = 'Please select category!'  
                messages.warning(request, user_added_warning)
                return redirect(request.META.get('HTTP_REFERER'))
            
            menu_addons = request.POST.getlist('selected_item_cat_dropdown_addons') or None
            print("selected addons",menu_addons)
        
            
            menu_description = request.POST.get('menu_description') or None
            print("menu_description",menu_description)

            if menu_description is None:
                user_added_warning = 'Please enter description!'  
                messages.warning(request, user_added_warning)
                return redirect(request.META.get('HTTP_REFERER'))
            if menu_description:
                menu_description = cleanhtml(menu_description)
            

            category_instance = MenuCategory.objects.filter(id = selected_menu_cat).first()


            menu_instance = Menu.objects.create(title = menu_name,total_price = menu_price, description=menu_description,category= category_instance)
            menu_instance.save()
            menu_instance.dicounted_price= discounted_price
            if int(category_instance.menu_count) > 1:
                dgdjdh = {} 
                for i in range(int(category_instance.menu_count)):
                    
                    key = f"{i + 1}"
                    dhfg = None
                    dgdjdh[str(key)] = str(dhfg)

                menu_instance.associated_items = json.dumps(dgdjdh)
                menu_instance.save()
            else:
                pass


            #  linking addon
            if menu_addons:
                add_ons = Alladdson.objects.filter(id__in =menu_addons)

                for add_on in add_ons:
                    
                    add_on.menu.add(menu_instance)
                    add_on.save()

            else:
                menu_instance.menu_addson_records.clear()



            



            # Send Data message
            list_of_fcm = list(Orders.objects.values_list('order_fcm', flat=True).distinct())
            print("list_of_fcm", list_of_fcm)

            
            for token in list_of_fcm:
                try:
                    extra = {"newData": "2"}
                    send_salient_data_message(token, extra)
                except Exception as e:
                    print("Error:", e)
            # End Send Data message

            

            
            


            group_added_success = 'Menu' + ' ' + menu_instance.title + ' ' + 'added successfully !'  
            messages.success(request, group_added_success)
            
                
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'dashboard/permission_denied.html')



def EditMenuForm(request,id,add_button_clicked=None):
    
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'Menus'  in chk or request.user.is_superuser:
        re_render = False
        menu_instance = Menu.objects.filter(pk=id).first()
        selected_menu_category =[]
        selected_menu_category.append(menu_instance.category.title)
        print('chk kkkk selected_menu_category',selected_menu_category)
        menu_categories = MenuCategory.objects.all()

        all_addons = Alladdson.objects.all()
        menu_addons = list(Alladdson.objects.filter(item=menu_instance).values_list('id', flat=True))
        print("menu_addons",menu_addons)



        context= {'re_render':re_render,
                  'menu_instance':menu_instance,
                  'selected_menu_category':selected_menu_category,
                  'menu_categories':menu_categories,
                  'menu_addons':menu_addons,
                  'all_addons':all_addons
                  }
        return render(request, 'dashboard/Menus/edit_menu_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')



def EditMenu(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'Menus'  in chk or request.user.is_superuser:
        # re_render = False
        # post_data = request.POST
        


        update_menu_pk = request.POST.get('update_menu_pk') or None
        print("update_menu_pk",update_menu_pk)
        selected_menu_category = request.POST.get('selected_menu_category') or None
        print("selected_menu_category",selected_menu_category)
        
        # selcted_menu_flag = True

        # selected_menu_cat = request.POST.get('selected_menu_cat_dropdown') or None
        # print("selected_menu_cat",selected_menu_cat)

        # if selected_menu_cat is None:
        #     selcted_menu_flag = False
        # else:
        #     if not len(selected_menu_cat):
        #         selcted_menu_flag = False


        

        menu_name = request.POST.get('menu_name') or None
        print("menu_name",menu_name)

        if menu_name is None:
            user_added_warning = 'Please enter name!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        menu_price = request.POST.get('menu_price') or None
        print("menu_price",menu_price)

        if menu_price is None:
            user_added_warning = 'Please enter price!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        discounted_price = request.POST.get('discounted_price') or None
        print("discounted_price",discounted_price)

        # if selected_menu_cat is None:
        #     user_added_warning = 'Please select category!'  
        #     messages.warning(request, user_added_warning)
        #     return redirect(request.META.get('HTTP_REFERER'))

        menu_addons = request.POST.getlist('selected_item_cat_dropdown_addons') or None
        print("selected addons",menu_addons)
        
        menu_description = request.POST.get('menu_description') or None
        print("menu_description",menu_description)

        if menu_description is None:
            user_added_warning = 'Please enter description!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        if menu_description:
            menu_description = cleanhtml(menu_description)


        category_instance = MenuCategory.objects.filter(id = selected_menu_category).first()


        menu_instance = Menu.objects.filter(pk = update_menu_pk).first()

        menu_instance.title = menu_name
        menu_instance.total_price = menu_price
        menu_instance.description = menu_description
        menu_instance.category = category_instance
        menu_instance.dicounted_price = discounted_price

        menu_instance.save()

        #  linking addon
        if menu_addons:
            add_ons = Alladdson.objects.filter(id__in =menu_addons)

            for add_on in add_ons:
                
                add_on.menu.add(menu_instance)
                add_on.save()
        else:
            menu_instance.menu_addson_records.clear()


        # Send Data message
        list_of_fcm = list(Orders.objects.values_list('order_fcm', flat=True).distinct())
        print("list_of_fcm", list_of_fcm)

        for token in list_of_fcm:
            try:
                extra = {"newData": "2"}
                send_salient_data_message(token, extra)
            except Exception as e:
                print("Error:", e)
        # End Send Data message


        group_added_success = 'Menu' + ' ' + menu_instance.title + ' ' + 'updated successfully !'  
        messages.success(request, group_added_success)
            
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'dashboard/permission_denied.html')
    

def DeleteMenu(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Menus'  in chk or request.user.is_superuser:
    
        print("here for deleteing menu record")
        menu_id = request.GET.get("menu_id")    
        print("menu_id", menu_id)
        menu_instance = Menu.objects.filter(id=menu_id).first()
        menu_name = menu_instance.title

        menu_instance.delete() 
        # Send Data message
        list_of_fcm = list(Orders.objects.values_list('order_fcm', flat=True).distinct())
        print("list_of_fcm", list_of_fcm)

        for token in list_of_fcm:
            try:
                extra = {"newData": "2"}
                send_salient_data_message(token, extra)
            except Exception as e:
                print("Error:", e)
        # End Send Data message
        print("record deleted Successfully!")
        data = {'menu_name':menu_name}
        return JsonResponse(data)
    else:
        return render(request, 'dashboard/permission_denied.html')


# Item CRUD
def EditItemForm(request,id,add_button_clicked=None):
    
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'Menus'  in chk or request.user.is_superuser:
        re_render = False
        item_instance = Menuitems.objects.filter(pk=id).first()
        all_addons = Alladdson.objects.all()
        item_addons = list(Alladdson.objects.filter(item=item_instance).values_list('id', flat=True))
        print("item_addons",item_addons)

        context= {'re_render':re_render,
                  'item_instance':item_instance,
                  'all_addons':all_addons,
                  'item_addons':item_addons
                  
                  }
        return render(request, 'dashboard/Menus/edit_item_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')
    


def EditItem(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0 :
        return redirect('login-dashbaord')
    
    if 'Menus'  in chk or request.user.is_superuser:
        # re_render = False
        # post_data = request.POST
        


        update_item_pk = request.POST.get('update_item_pk') or None
        print("update_item_pk",update_item_pk)

        item_name = request.POST.get('item_name') or None
        print("item_name",item_name)

        if item_name is None:
            item_added_warning = 'Please enter name!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))

        item_price = request.POST.get('item_price') or None
        print("item_price",item_price)

        if item_price is None:
            item_added_warning = 'Please enter price!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        discounted_price = request.POST.get('discounted_price') or None
        print("discounted_price",discounted_price)
        
        # daily_deal = request.POST.getlist('membarh') or None
        # print("daily_deal",daily_deal)
        # add_ons = request.POST.getlist('membarh_ka') or None 
        # print("add_ons",add_ons)

        # if daily_deal or add_ons:
        #     pass
        # else: 
        #     item_added_warning = 'Please select item category!'  
        #     messages.warning(request, item_added_warning)
        #     return redirect(request.META.get('HTTP_REFERER'))


        item_image = request.FILES.get('item_image') or None
        print("item_image",item_image)


        if item_image:
            file_extension = item_image.name.split('.')[-1].lower()
            print("file extention", file_extension)
        
            if file_extension in ['png', 'jpg', 'jpeg', 'webp']:
                pass
            else:
                name_added_warning = 'Uplaod image file Only !'  
                messages.warning(request, name_added_warning)   
                return redirect(request.META.get('HTTP_REFERER'))
    
        

        items_addons = request.POST.getlist('selected_item_cat_dropdown_addons') or None
        print("selected addons",items_addons)

        item_description = request.POST.get('item_description') or None
        print("item_description",item_description)

        if item_description is None:
            item_added_warning = 'Please enter description!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        if item_description:
            item_description = cleanhtml(item_description)

        

        exclusive = request.POST.getlist('teckmarkinputbasicinput') or None 
        print("exclusive",exclusive)

        item_instance = Menuitems.objects.filter(pk=update_item_pk).first()

        item_instance.title = item_name
        item_instance.price = item_price
        item_instance.description = item_description

        
        item_instance.dicounted_price = discounted_price

        if item_image:
            item_instance.image = item_image

        
        
        item_instance.daily_deals = True
        item_instance.ads_on = False
        if exclusive is not None:
            # Menuitems.objects.filter(exclusive = True).update(exclusive = False)
            item_instance.exclusive = True
        else:
            item_instance.exclusive = False
        

        item_instance.save()

        #  linking addon
        if items_addons:
            add_ons = Alladdson.objects.filter(id__in =items_addons)

            for add_on in add_ons:
                
                add_on.item.add(item_instance)
                add_on.save()
        else:
            item_instance.item_addson_records.clear()

        # Send Data message
        list_of_fcm = list(Orders.objects.values_list('order_fcm', flat=True).distinct())
        print("list_of_fcm", list_of_fcm)

        for token in list_of_fcm:
            try:
                extra = {"newData": "1"}
                send_salient_data_message(token, extra)
            except Exception as e:
                print("Error:", e)
        # End Send Data message

        


        item_added_success = 'Item' + ' ' + item_instance.title + ' ' + 'updated successfully !'  
        messages.success(request, item_added_success)
        
            
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'dashboard/permission_denied.html')
    

# Delete Item Image
def DeleteItemImage(request,id):
    item_id = request.GET.get("item_id") 
    print("item_id",item_id)
    profile_pic_flag = True
    item_instance = Menuitems.objects.filter(pk=item_id).first()
    if item_instance.image is None:
        profile_pic_flag = False
    else:
        if not item_instance.image:
            profile_pic_flag = False
        else:
            item_instance.image.delete(save=False)
            item_instance.save() 
    data = {'user_name':item_instance.title,'profile_pic_flag':profile_pic_flag}
    return JsonResponse(data)


def AddItemForm(request,add_button_clicked=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'Menus'  in chk or request.user.is_superuser:
        re_render = False
        all_addons = Alladdson.objects.all()


        
        context= {'re_render':re_render,
                  'all_addons':all_addons}
        return render(request, 'dashboard/Menus/add_item_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')
    


def AddItem(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'Menus'  in chk or request.user.is_superuser :

        
        
        item_name = request.POST.get('item_name') or None
        print("item_name",item_name)

        if item_name is None:
            item_added_warning = 'Please enter name!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        

        item_price = request.POST.get('item_price') or None
        print("item_price",item_price)

        if item_price is None:
            item_added_warning = 'Please enter price!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        discounted_price = request.POST.get('discounted_price')
        print("discounted_price",discounted_price)

        # daily_deal = request.POST.getlist('membarh') or None 
        # print("daily_deal",daily_deal)
        # add_ons = request.POST.getlist('membarh_ka') or None 
        # print("add_ons",add_ons)

        # if daily_deal or add_ons:
        #     pass
        # else: 
        #     item_added_warning = 'Please select item category!'  
        #     messages.warning(request, item_added_warning)
        #     return redirect(request.META.get('HTTP_REFERER'))
        
        exclusive = request.POST.getlist('teckmarkinputbasicinput') or None 
        print("exclusive",exclusive)



        item_image = request.FILES.get('item_image') or None

        
           
        if item_image is not  None:  
            if item_image.content_type.startswith('image'):
                pass
            else:
                item_added_warning = 'Please image file !'  
                messages.warning(request, item_added_warning)
                return redirect(request.META.get('HTTP_REFERER')) 
        else: 
            
            item_added_warning = 'Please upload image!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER')) 
            
        

        items_addons = request.POST.getlist('selected_item_cat_dropdown_addons') or None
        print("selected addons",items_addons)

        item_description = request.POST.get('item_description') or None
        print("item_description",item_description)

        if item_description is None:
            item_added_warning = 'Please enter description!'  
            messages.warning(request, item_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        

        if item_description:
            item_description = cleanhtml(item_description)

        item_instance = Menuitems.objects.create(title = item_name,price = item_price, image = item_image, description=item_description)
        item_instance.save()

        if discounted_price:
            item_instance.dicounted_price = discounted_price

        
        item_instance.daily_deals = True
        item_instance.ads_on = False
        if exclusive is not None:
            # Menuitems.objects.filter(exclusive = True).update(exclusive = False)
            item_instance.exclusive = True
        else:
            item_instance.exclusive = False


        

        item_instance.save()

        #  linking addon
        if items_addons:
            add_ons = Alladdson.objects.filter(id__in =items_addons)

            for add_on in add_ons:
                
                add_on.item.add(item_instance)
                add_on.save()
        else:
            item_instance.item_addson_records.clear()


        # Send Data message
        list_of_fcm = list(Orders.objects.values_list('order_fcm', flat=True).distinct())
        print("list_of_fcm", list_of_fcm)

        for token in list_of_fcm:
            try:
                extra = {"newData": "1"}
                send_salient_data_message(token, extra)
            except Exception as e:
                print("Error:", e)
        # End Send Data message


        item_added_success = 'Item' + ' ' + item_instance.title + ' ' + 'added successfully !'  
        messages.success(request, item_added_success)
        
            
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'dashboard/permission_denied.html')
    



def Itemlist(request):  
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'Menus'  in chk or request.user.is_superuser:

        all_items = Menuitems.objects.exists()
        if not all_items:
            ven = "Not Found"
            
            
        else: 
            p = Paginator(Menuitems.objects.order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
            
        context = {'ven':ven }
        return render(request, 'dashboard/Menus/items_list.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')
    


def DeleteItem(request,id=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Menus'  in chk or request.user.is_superuser:
    
        print("here for deleteing item record")
        item_id = request.GET.get("item_id")    
        print("item_id", item_id)
        item_instance = Menuitems.objects.filter(id=item_id).first()
        item_name = item_instance.title

        item_instance.delete() 
        # Send Data message
        list_of_fcm = list(Orders.objects.values_list('order_fcm', flat=True).distinct())
        print("list_of_fcm", list_of_fcm)

        for token in list_of_fcm:
            try:
                extra = {"newData": "1"}
                send_salient_data_message(token, extra)
            except Exception as e:
                print("Error:", e)
        # End Send Data message
        print("record deleted Successfully!")
        data = {'item_name':item_name}
        return JsonResponse(data)
    else:
        return render(request, 'dashboard/permission_denied.html')
    




# items Associated with menu.....
import json

def MenuItemDetail(request,id):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Menus'  in chk or request.user.is_superuser:
        menu_instance = Menu.objects.filter(pk =id).first()
        print("category id ",menu_instance.category.pk)
        category_id = menu_instance.category.pk
        total_count = menu_instance.category.menu_count
        daily_flag = True
        if menu_instance.category.menu_count > 1:

            daily_flag = False
            menu_items = json.decoder.JSONDecoder().decode(menu_instance.associated_items)
        else:
            menu_items = None


        print("menu_items",menu_items)

        all_items = Menuitems.objects.filter(daily_deals = True).all()
        print("all_items",all_items)



        context = {'total_count': range(total_count),
                'menu_instance':menu_instance,
                'menu_items' :menu_items,
                'all_items':all_items,
                'daily_flag':daily_flag,
                'category_id':category_id
                
                }

        return render(request, 'dashboard/Menus/menu_item_detail.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')



# Add associated item

def AddAssociatedItemMenuForm(request,id,counter):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    if 'Menus'  in chk or request.user.is_superuser:
        all_items = Menuitems.objects.filter(daily_deals = True).all()

        menu_id = id 
        dict_key = counter

        
        context = {'all_items':all_items,
                'menu_id':menu_id,
                'dict_key':dict_key
                
                }

        return render(request, 'dashboard/Menus/add_associate_item_menu.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')


def AddAssociatedItemMenu(request):

    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    if 'Menus'  in chk or request.user.is_superuser:

        if request.method == 'POST':

            menu_id = request.POST.get('menu_id') or None
            print("menu_id",menu_id)

            if menu_id is None:
                item_added_warning = 'Please select any menu first!'  
                messages.warning(request, item_added_warning)
                return redirect(request.META.get('HTTP_REFERER'))

            item_id = request.POST.get('selected_item_cat_dropdown') or None
            print("item_id",item_id)

            if item_id is None:
                item_added_warning = 'Please select any item first!'  
                messages.warning(request, item_added_warning)
                return redirect(request.META.get('HTTP_REFERER'))


            dict_key = request.POST.get('dict_key') or None
            print("dict_key",dict_key)

            menu_instance = Menu.objects.filter(id = menu_id ).first()

            menu_items = json.decoder.JSONDecoder().decode(menu_instance.associated_items)

            print("menu_items check 1",menu_items)


            menu_items[str(dict_key)] = str(item_id)

            menu_instance.associated_items = json.dumps(menu_items)



            menu_instance.save()

            print("menu_items check 2",menu_items)


            item_added_success = 'Item added successfully !'  
            messages.success(request, item_added_success)
            
            
            url = f'menu_item_detail/{menu_id}'

            return HttpResponseRedirect(url)    
    else:
        return render(request, 'dashboard/permission_denied.html')
        
def EditAssociatedItemMenuForm(request,id,counter):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    if 'Menus'  in chk or request.user.is_superuser:
        all_items = Menuitems.objects.filter(daily_deals = True).all()

        dict_key = counter
        menu_id = id 

        menu_instance = Menu.objects.filter(id = id).first()
        menu_items = json.decoder.JSONDecoder().decode(menu_instance.associated_items)

        print("menu_items check 1",menu_items)


        selected_item_id = menu_items[str(dict_key)]

        print("selected_item_id", selected_item_id)

        item_instance =Menuitems.objects.filter(id = selected_item_id).first()

        selected_item_title = item_instance.title

        
        
        context = {'all_items':all_items,
                'menu_id':menu_id,
                'dict_key':dict_key,
                'selected_item_title':selected_item_title
                
                }

        return render(request, 'dashboard/Menus/edit_associate_item_menu.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')




def EditssociatedItemMenu(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    if 'Menus'  in chk or request.user.is_superuser:

        if request.method == 'POST':

            menu_id = request.POST.get('menu_id') or None
            print("menu_id",menu_id)

            item_id = request.POST.get('selected_item_cat_dropdown') or None
            print("item_id",item_id)

            dict_key = request.POST.get('dict_key') or None
            print("dict_key",dict_key)

            menu_instance = Menu.objects.filter(id = menu_id ).first()

            menu_items = json.decoder.JSONDecoder().decode(menu_instance.associated_items)

            print("menu_items check 1",menu_items)


            menu_items[str(dict_key)] = str(item_id)

            menu_instance.associated_items = json.dumps(menu_items)



            menu_instance.save()

            print("menu_items check 2",menu_items)


            item_added_success = 'Item updated successfully !'  
            messages.success(request, item_added_success)
            
            
            url = f'menu_item_detail/{menu_id}'

            return HttpResponseRedirect(url)    
    else:
        return render(request, 'dashboard/permission_denied.html')






def AddMenuCategoryForm(request,add_button_clicked=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'Menus'  in chk  or request.user.is_superuser:
        re_render = False
        

        
        context= {'re_render':re_render}
        return render(request, 'dashboard/Menus/add_menu_category_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')
    


def AddMenuCategory(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'Menus'  in chk or request.user.is_superuser:
        if request.method == 'POST':
            
            menu_category_name = request.POST.get('menu_category_name') or None
            print("menu_category_name",menu_category_name)


            if menu_category_name is None:
                user_added_warning = 'Please enter name!'  
                messages.warning(request, user_added_warning)
                return redirect(request.META.get('HTTP_REFERER'))

            menu_category_count = request.POST.get('menu_category_count') or None
            print("menu_category_count",menu_category_count)

            if menu_category_count is None:
                user_added_warning = 'Please enter days count!'  
                messages.warning(request, user_added_warning)
                return redirect(request.META.get('HTTP_REFERER'))

            
            
            if MenuCategory.objects.filter(menu_count = menu_category_count).exists():
                user_added_warning = 'Category with this menu cout already exixts!'  
                messages.warning(request, user_added_warning)
                return redirect(request.META.get('HTTP_REFERER'))
            

            kitchen_share_percentage = request.POST.get('kitchen_share_percentage') or None
            print("kitchen_share_percentage",kitchen_share_percentage)


            if kitchen_share_percentage is None:
                user_added_warning = 'Please enter kitchen share!'  
                messages.warning(request, user_added_warning)
                return redirect(request.META.get('HTTP_REFERER'))
            
            menu_category_description = request.POST.get('menu_category_description') or None
            print("menu_category_description",menu_category_description)

            
            if menu_category_description:
                menu_category_description = cleanhtml(menu_category_description)
            

            menu_category_instance = MenuCategory.objects.create(title = menu_category_name,menu_count= menu_category_count,Kitchen_share_percent=kitchen_share_percentage )
            menu_category_instance.save()


            group_added_success = 'Category' + ' ' + menu_category_instance.title + ' ' + 'added successfully !'  
            messages.success(request, group_added_success)
            
                
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'dashboard/permission_denied.html')
    



def EditMenuCategoryForm(request,id,add_button_clicked=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print("chk",chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'Menus'  in chk or request.user.is_superuser:
        re_render = False
        menu_category_instance = MenuCategory.objects.filter(pk=id).first()
        

        
        context= {'re_render':re_render,
                  'menu_category_instance':menu_category_instance
                  }
        return render(request, 'dashboard/Menus/edit_menu_category_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')
    



def EditMenuCategory(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print("chk", chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'Menus'  in chk or request.user.is_superuser:
        
        


        update_menu_category_pk = request.POST.get('update_menu_category_pk') or None
        print("update_menu_category_pk",update_menu_category_pk)


        menu_category_name = request.POST.get('menu_category_name') or None
        print("menu_category_name",menu_category_name)


        if menu_category_name is None:
            user_added_warning = 'Please enter name!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))

        menu_category_count = request.POST.get('menu_category_count') or None
        print("menu_category_count",menu_category_count)

        if menu_category_count is None:
            user_added_warning = 'Please enter days count!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        

        kitchen_share_percentage = request.POST.get('kitchen_share_percentage') or None
        print("kitchen_share_percentage",kitchen_share_percentage)


        if kitchen_share_percentage is None:
            user_added_warning = 'Please enter kitchen share!'  
            messages.warning(request, user_added_warning)
            return redirect(request.META.get('HTTP_REFERER'))
        
        menu_category_description = request.POST.get('menu_category_description') or None
        print("menu_category_description",menu_category_description)

        
        if menu_category_description:
            menu_category_description = cleanhtml(menu_category_description)

        menu_category_instance = MenuCategory.objects.filter(pk = update_menu_category_pk).first()

        menu_category_instance.title = menu_category_name
        menu_category_instance.menu_count = menu_category_count
        menu_category_instance.Kitchen_share_percent = kitchen_share_percentage

        menu_category_instance.save()


        group_added_success = 'Category' + ' ' + menu_category_instance.title + ' ' + 'updated successfully !'  
        messages.success(request, group_added_success)
            
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'dashboard/permission_denied.html')



def DeleteMenuCategory(request,id=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Menus'  in chk or request.user.is_superuser:
    
        print("here for deleteing item record")
        menu_category_id = request.GET.get("cat_id")    
        print("menu_category_id", menu_category_id)
        menu_category_instance = MenuCategory.objects.filter(id=menu_category_id).first()
        cat_name = menu_category_instance.title

        menu_category_instance.delete() 
        print("record deleted Successfully!")
        data = {'cat_name':cat_name}
        return JsonResponse(data)
    else:
        return render(request, 'dashboard/permission_denied.html')
    

def OrderItemsListingPage(request):

    if 'user_data' in  request.session:
        print("g")
    elif 'soc_loged' in  request.session: 
        print("f")  
    elif 'lnkd_loged' in  request.session:
        print("l")
    else:
        return redirect('sign_in')

    all_items = Menuitems.objects.filter(daily_deals = True).all()
    context= {'all_items':all_items}

    return render(request, 'dashboard/Menus/item_listing_page.html', context)


def ItemOrderForm(request,id,add_button_clicked=None):

    if 'user_data' in  request.session:
        print("g")
    elif 'soc_loged' in  request.session: 
        print("f")  
    elif 'lnkd_loged' in  request.session:
        print("l")
    else:
        return redirect('sign_in')

    selected_item = Menuitems.objects.filter(id= id).first()

    all_add_ons_items = Menuitems.objects.filter(ads_on = True)

    print("all_add_ons_items",all_add_ons_items)

    re_render = False

    print("add_button_clicked", add_button_clicked)
    if add_button_clicked:
        if '_old_post' in request.session:
            del request.session['_old_post']
        request.session['_old_post'] = None
    
    old_post = request.session.get('_old_post')
    print("data in old post is sub tile re render case ", old_post)
    if old_post is not None:
        re_render = True
           


        context= {'selected_item':selected_item,
            'all_add_ons_items':all_add_ons_items,
            're_render':re_render,
            'customer_name': old_post['customer_name'],
            'customer_email': old_post['customer_email'],
            'order_details': old_post['order_details'],
            'customer_address': old_post['customer_address'],
            
            
            }

    else:


        context= {'selected_item':selected_item,
                'all_add_ons_items':all_add_ons_items,
                're_render':re_render
                
                }

    return render(request, 'dashboard/Menus/item_order_placing_form.html', context)

from webApp.views.Others.geocode_address import *
from django.urls import reverse

def SubmitItemOrderForm(request):

    if request.method == 'POST':

        re_render = False
        post_data = request.POST
        selected_item_id = request.POST.get('selected_item_id') or None
        # print("selected_item_id",selected_item_id)


        customer_name = request.POST.get('customer_name') or None
        # print("customer_name",customer_name)
        if customer_name is None:
            order_added_warning = 'Please enter name!'  
            messages.warning(request, order_added_warning) 
            if '_old_post' in request.session:
                del request.session['_old_post']
            old_data = {}
            old_data['customer_name'] = post_data['customer_name']  
            old_data['selected_item_id'] = post_data['selected_item_id'] 
             
            old_data['order_details'] = post_data['order_details'] 
            old_data['customer_address'] = post_data['customer_address']
            old_data['total_price'] = post_data['total_price']
            # old_data['selected_addons'] = request.POST.getlist('selected_addons') or None   
            

            print("old data", old_data)
            request.session['_old_post'] = old_data
            add_button_clicked = 0
            url = f'item_order_placing_form/{selected_item_id}/{add_button_clicked}'
            return HttpResponseRedirect(url)
            # return redirect(request.META.get('HTTP_REFERER'))

        customer_email = request.POST.get('customer_email') or None
        # print("customer_email",customer_email)
        if customer_email is None:
            order_added_warning = 'Please enter email!'  
            messages.warning(request, order_added_warning) 
            if '_old_post' in request.session:
                del request.session['_old_post']
            old_data = {}
            old_data['customer_name'] = post_data['customer_name']  
            old_data['selected_item_id'] = post_data['selected_item_id'] 
            old_data['customer_email'] = post_data['customer_email'] 
             
            old_data['order_details'] = post_data['order_details'] 
            old_data['customer_address'] = post_data['customer_address']
            old_data['total_price'] = post_data['total_price']
            # old_data['selected_addons'] = request.POST.getlist('selected_addons') or None   
            

            print("old data", old_data)
            request.session['_old_post'] = old_data
            add_button_clicked = 0
            url = f'item_order_placing_form/{selected_item_id}/{add_button_clicked}'
            return HttpResponseRedirect(url)
            # return redirect(request.META.get('HTTP_REFERER'))

        customer_address = request.POST.get('customer_address') or None
        # print("customer_address",customer_address)
        if customer_address is None:
            order_added_warning = 'Please enter address!'  
            messages.warning(request, order_added_warning) 
            if '_old_post' in request.session:
                del request.session['_old_post']
            old_data = {}
            old_data['customer_name'] = post_data['customer_name']  
            old_data['selected_item_id'] = post_data['selected_item_id'] 
             
            old_data['order_details'] = post_data['order_details'] 
            old_data['customer_address'] = post_data['customer_address']
            old_data['total_price'] = post_data['total_price']
            # old_data['selected_addons'] = request.POST.getlist('selected_addons') or None   
            

            print("old data", old_data)
            request.session['_old_post'] = old_data
            add_button_clicked = 0
            url = f'item_order_placing_form/{selected_item_id}/{add_button_clicked}'
            return HttpResponseRedirect(url)
            # return redirect(request.META.get('HTTP_REFERER'))

        selected_item_price = request.POST.get('selected_item_price') or None


        order_details = request.POST.get('order_details') or None
        # print("order_details",order_details)

        selected_item_id = request.POST.get('selected_item_id') or None
        # print("selected_item_id",selected_item_id)

        selected_addon_ids = request.POST.getlist('selected_addons[]') or None

        # print(selected_addon_ids)
        my_list = selected_addon_ids

        total_price = request.POST.get('total_price') or None
        # print("total_price",total_price)


        # get the records of all the add_on_items 

        lat = None

        try:
            lat, long = OpenCage_for_address(customer_address)
            print("order lat long",lat,long)
        except:
            order_address_warning = 'This address cannot be located please enter valid one !'  
              
            messages.warning(request, order_address_warning) 
            if '_old_post' in request.session:
                del request.session['_old_post']
            old_data = {}
            old_data['customer_name'] = post_data['customer_name']  
            old_data['selected_item_id'] = post_data['selected_item_id'] 
            old_data['customer_email'] = post_data['customer_email'] 
            old_data['order_details'] = post_data['order_details'] 
            old_data['customer_address'] = post_data['customer_address']
            old_data['total_price'] = post_data['total_price']
            old_data['addon_items_list'] = request.POST.getlist('selected_addons[]') or None   
            

            print("old data", old_data)
            request.session['_old_post'] = old_data
            add_button_clicked = 0
            url = f'item_order_placing_form/{selected_item_id}/{add_button_clicked}'
            return HttpResponseRedirect(url)
            # return redirect(request.META.get('HTTP_REFERER')) 
            

        if lat is None:
            order_address_warning = 'This address cannot be located please enter valid one !' 
              
            messages.warning(request, order_address_warning) 
            if '_old_post' in request.session:
                del request.session['_old_post']
            old_data = {}
            old_data['customer_name'] = post_data['customer_name']  
            old_data['selected_item_id'] = post_data['selected_item_id'] 
            old_data['customer_email'] = post_data['customer_email'] 
            old_data['order_details'] = post_data['order_details'] 
            old_data['customer_address'] = post_data['customer_address']
            old_data['total_price'] = post_data['total_price']
            old_data['addon_items_list'] = request.POST.getlist('selected_addons[]') or None   
            

            print("old data", old_data)
            request.session['_old_post'] = old_data
            add_button_clicked = 0
            url = f'item_order_placing_form/{selected_item_id}/{add_button_clicked}'
            return HttpResponseRedirect(url)
            # return redirect(request.META.get('HTTP_REFERER'))
            
        
        try:
            # print("here in try")
            order_kitchen,the_distance = lat_long_nearest_kitchen(lat,long)
            if  order_kitchen  == 3276:
                order_address_warning = 'Not operate in your area!'
                messages.warning(request, order_address_warning) 
                if '_old_post' in request.session:
                    del request.session['_old_post']
                old_data = {}
                old_data['customer_name'] = post_data['customer_name']  
                old_data['selected_item_id'] = post_data['selected_item_id'] 
                old_data['customer_email'] = post_data['customer_email'] 
                old_data['order_details'] = post_data['order_details'] 
                old_data['customer_address'] = post_data['customer_address']
                old_data['total_price'] = post_data['total_price']
                old_data['addon_items_list'] = request.POST.getlist('selected_addons[]') or None   
                

                print("old data", old_data)
                request.session['_old_post'] = old_data
                add_button_clicked = 0
                url = f'item_order_placing_form/{selected_item_id}/{add_button_clicked}'
                return HttpResponseRedirect(url)
                
            elif  order_kitchen  is None:
                order_address_warning = 'Unfortunately no active kitchen today!'
                messages.warning(request, order_address_warning) 
                if '_old_post' in request.session:
                    del request.session['_old_post']
                old_data = {}
                old_data['customer_name'] = post_data['customer_name']  
                old_data['selected_item_id'] = post_data['selected_item_id'] 
                old_data['customer_email'] = post_data['customer_email'] 
                old_data['order_details'] = post_data['order_details'] 
                old_data['customer_address'] = post_data['customer_address']
                old_data['total_price'] = post_data['total_price']
                old_data['addon_items_list'] = request.POST.getlist('selected_addons[]') or None   
                

                print("old data", old_data)
                request.session['_old_post'] = old_data
                add_button_clicked = 0
                url = f'item_order_placing_form/{selected_item_id}/{add_button_clicked}'
                return HttpResponseRedirect(url)
                
        except:
            order_kitchen = None


        order_instance = Orders.objects.create(user = customer_email, customer_name=customer_name, address_details=customer_address,latitude=lat,longitude=long, total_price=total_price,kitchen_id=order_kitchen)

        order_instance.save()  
        orderitem_instance = OrderItems.objects.create(order = order_instance, item_id = selected_item_id, extra_details= order_details, sub_total= selected_item_price )
        orderitem_instance.save()

        

        if selected_addon_ids is not None:
            final_addon_list = list(set(selected_addon_ids))
            # print(final_addon_list)

            for item in final_addon_list: 
                # print("id",item)
                count = my_list.count(str(item))
                # print("count",count)
                OrderAddson.objects.create(order = order_instance, item_id = item, quantity =count) 


        # # Send WebSocket notification
        async_to_sync(channel_layer.group_send)(
            'orders_listing_group',
            {
                'type': 'send_order_list_notification',
                'message': f'Order {order_instance.pk} has been submitted!'
            }
        )

        redirect_url = reverse('order_confirmation', args=[order_instance.pk])
        return redirect(redirect_url)
        
    



# Item Search
def  ItemCustomSearch(request): 
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'Menus'  in chk or request.user.is_superuser:
        print("here in item custom search")
        item = request.GET.get('item') or None   
        print("item", item)
        searched_item_exist = Menuitems.objects.filter(title__icontains=item).exists()
        if searched_item_exist:    
            searched_item = list(Menuitems.objects.filter(title__icontains=item).values()) 
            print("list of item",searched_item) 
            
            context = {'ven':  searched_item}  
            return JsonResponse({"success": True,"response":context}) 
        else:  
            return JsonResponse({"success": False})
    else:
        return render(request, 'dashboard/permission_denied.html')

    

    

# Search Menu
def  MenuCustomSearch(request): 
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'Menus'  in chk or request.user.is_superuser:
        print("here in Menu custom search")
        cat_id = request.GET.get('cat_id') or None   
        print("cat_id", cat_id)
        menu = request.GET.get('menu') or None   
        print("menu", menu)
        searched_menu_exist = Menu.objects.filter(title__icontains=menu).filter(category_id = cat_id).exists()
        if searched_menu_exist:    
            searched_menu = list(Menu.objects.filter(title__icontains=menu).filter(category_id = cat_id).values()) 
            print("list of menus:",searched_menu) 
            
            context = {'ven':  searched_menu}  
            return JsonResponse({"success": True,"response":context}) 
        else:  
            return JsonResponse({"success": False})
    else:
        return render(request, 'dashboard/permission_denied.html')


# Order Confirmation 

def OrderConfirmation(request,id):
    print("order id :",id)
    order_instance = Orders.objects.filter(id = id).first()

    Accounts = Paymentaccounts.objects.filter(user__is_superuser=True).all()
    print("Accounts",Accounts)

    context= {"order_instance":order_instance,
              "Accounts":Accounts
                }

    return render(request, 'dashboard/Menus/order_confirm_page.html', context)




    

    
