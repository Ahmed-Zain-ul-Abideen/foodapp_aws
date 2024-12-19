from django.shortcuts import render,redirect, HttpResponseRedirect
from webApp.models import *
from django.contrib import messages
from django.core.paginator import Paginator
from geopy.geocoders import Nominatim
from django.http import JsonResponse
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth import logout
from webApp.templatetags.webApp_extras import user_role
from webApp.forms import  *
from webApp.views.Others.geocode_address import *


def  Chefregisteration(request,id):
    id = id[4:]
    id = id[:-4]
    print(id)
    if Kitchen.objects.filter(pk=id).filter(approved_owner=None).exists():
        if request.method == 'POST':
            form = ChefRegistrationForm(request.POST)
            if form.is_valid():
                # form.save()
                chef_user = User.objects.create_user(username=request.POST.get('username'),password=request.POST.get('password2'),is_staff=1)
                chef_user.save()
                chef_group = Group.objects.filter(name="Kitchen").first()
                chef_user.groups.add(chef_group)
                chef_user.save()
                chef_kitchen = Kitchen.objects.filter(pk=id).first()
                chef_kitchen.approved_owner_id = chef_user.id 
                chef_kitchen.save()

                chef_user.first_name = chef_kitchen.owner
                chef_user.email = chef_kitchen.email
                chef_user.save()
                return redirect('login-dashboard')  # Redirect to login page after successful registration
        else:
            form = ChefRegistrationForm()
        return render(request, 'dashboard/Users/chefregister.html', {'form': form})
    elif request.user.is_authenticated:
        return redirect('index')
    else:
        return redirect('login-dashboard')
    

def  SaveAdminAddress(request,add=None):
    if not request.user.is_authenticated:
      return redirect('login-dashboard')
    chk = user_role(request.user)
     
    if len(chk) == 0:
      return render(request, 'dashboard/permission_denied_updt.html')  
    elif len(chk) == 1 :
      return render(request, 'dashboard/permission_denied_updt.html')
    # elif AdminAddress.objects.filter(admin_address=request.user.id).exists():

    #     return redirect('index') 
    elif not 'Admin'  in chk :
        return render(request, 'dashboard/permission_denied_updt.html')
    if request.method == 'POST':
        form = AdminAddressForm(request.POST)
        if AdminAddress.objects.filter(admin_address_id=request.user.id).exists(): 
            if form.is_valid():
                if  AdminAddress.objects.filter(admin_address_id=request.user.id).filter(address_details=request.POST.get('address_details')).exists():
                    print("same address as before")
                    return redirect(request.META.get('HTTP_REFERER')) 
                else:
                    try:
                        lat, long = OpenCage_for_address(request.POST.get('address_details'))
                    except:
                        return render(request, 'dashboard/Users/Adminaddress.html', {'form': form})
                    print("lat opncg,long opncg",lat,long)
                    if lat is None:
                        return render(request, 'dashboard/Users/Adminaddress.html', {'form': form})
                    
                    admn_ktchns_ids = []
                    if  Kitchen.objects.filter(kitchen_admin=request.user.id).exists():
                        admn_ktchns_ids = list(Kitchen.objects.filter(kitchen_admin=request.user.id).values_list('pk',flat=True))
                        admn_ktchns_adres = KitchenAddress.objects.filter(Kitchen_id__in=admn_ktchns_ids)
                        for kithnadres in admn_ktchns_adres:
                            kitchen_admin = lat_long_nearest_admin(kithnadres.latitude,kithnadres.longitude)
                            if kitchen_admin is None:
                                pass
                            else:
                                kitchn_inst = Kitchen.objects.filter(pk=kithnadres.Kitchen_id).first()
                                kitchn_inst.kitchen_admin = kitchen_admin
                                kitchn_inst.save()
                    else:

                        other_kitchens_ids = list(Kitchen.objects.exclude(pk__in=admn_ktchns_ids).values_list('pk',flat=True))

                        if len(other_kitchens_ids):

                            other_ktchns_adres = KitchenAddress.objects.filter(Kitchen_id__in=other_kitchens_ids)
                            for kithnadres in other_ktchns_adres:
                                kitchen_admin = lat_long_nearest_admin(kithnadres.latitude,kithnadres.longitude)
                                if kitchen_admin is None:
                                    pass
                                else:
                                    kitchn_inst = Kitchen.objects.filter(pk=kithnadres.Kitchen_id).first()
                                    kitchn_inst.kitchen_admin = kitchen_admin
                                    kitchn_inst.save()




                    admin_address_instance = AdminAddress.objects.filter(admin_address_id=request.user.id).first()  
                    admin_address_instance.address_details = request.POST.get('address_details')
                    admin_address_instance.latitude = lat
                    admin_address_instance.longitude = long
                    admin_address_instance.save()
                    return redirect(request.META.get('HTTP_REFERER'))
        else: 
            if form.is_valid():  
                try:
                    lat, long = OpenCage_for_address(request.POST.get('address_details'))
                except:
                    return render(request, 'dashboard/Users/Adminaddress.html', {'form': form})
                print("lat opncg,long opncg",lat,long)
                if lat is None:
                    return render(request, 'dashboard/Users/Adminaddress.html', {'form': form})
                admin_address_instance = AdminAddress.objects.create(latitude=lat,longitude=long,admin_address_id=request.user.id,address_details=request.POST.get('address_details'))
                admin_address_instance.save() 
                form = AdminAddressForm(instance=admin_address_instance)

                other_kitchens_ids = list(Kitchen.objects.all().values_list('pk',flat=True))
                if len(other_kitchens_ids):

                    other_ktchns_adres = KitchenAddress.objects.filter(Kitchen_id__in=other_kitchens_ids)
                    for kithnadres in other_ktchns_adres:
                        kitchen_admin = lat_long_nearest_admin(kithnadres.latitude,kithnadres.longitude)
                        if kitchen_admin is None:
                            pass
                        else:
                            kitchn_inst = Kitchen.objects.filter(pk=kithnadres.Kitchen_id).first()
                            kitchn_inst.kitchen_admin = kitchen_admin
                            kitchn_inst.save()
                # return redirect(request.META.get('HTTP_REFERER')) 
                # admin_address_instance = AdminAddress.objects.create(latitude=lat,longitude=long,admin_address=request.user.id,address_line1=request.POST.get('address_line1'),address_line2=request.POST.get('address_line2'),city=request.POST.get('city'),country=request.POST.get('country'),postal_code=request.POST.get('postal_code'))
                # admin_address_instance.save() 
                # return redirect('index')  # Redirect to login page after successful registration
    else:
        if add == "None":
            form = AdminAddressForm()
        else:
            form = AdminAddressForm(instance=AdminAddress.objects.filter(admin_address_id=request.user.id).first())
    return render(request, 'dashboard/Users/Adminaddress.html', {'form': form})
     
         


# Search User
def  UserCustomSearch(request): 
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Users'  in chk or request.user.is_superuser:
    

        print("here in kitchen custom search")
        user_instance = request.GET.get('users') or None   
        print("user_instance", user_instance)
        searched_user_exist = User.objects.filter(username__icontains=user_instance).exists()
        if searched_user_exist:    
            searched_users = list(User.objects.filter(username__icontains=user_instance).values()) 
            print("list of kitchens",searched_users) 
            
            context = {'ven':  searched_users}  
            return JsonResponse({"success": True,"response":context}) 
        else:  
            return JsonResponse({"success": False})
    else:
        return render(request, 'dashboard/permission_denied.html')



def Userlist(request):  
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Users'  in chk or request.user.is_superuser:
    
        all_user = User.objects.exists()
        if not all_user:
            ven = "Not Found"
            
        else: 
            p = Paginator(User.objects.all().order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        context = {'ven':ven}
        return render(request, 'dashboard/Users/index.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')
    


def DeleteUser(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Users'  in chk or request.user.is_superuser:
    
    
        print("here for deleteing user record")
        user_id = request.GET.get("user_id")    
        print("user_id", user_id)
        user_instance = User.objects.filter(id=user_id).first()
        username = user_instance.username

        user_instance.delete() 
        print("record deleted Successfully!")
        data = {'username':username}
        return JsonResponse(data)
    else:
        return render(request, 'dashboard/permission_denied.html')


    
def AddUserForm(request,add_button_clicked=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Users'  in chk or request.user.is_superuser:
        re_render = False

        if add_button_clicked:
            if '_old_post' in  request.session:
                del request.session['_old_post']    
                request.session['_old_post'] = None

        old_post = request.session.get('_old_post')
        print("data in old post is", old_post)

        if old_post is not None:
            print('username',old_post['username'])
            if old_post['username'] == 'None':
                 
                 old_post['username'] = ''

            re_render = True
            context= {'re_render':re_render, 
                    'first_name': old_post['first_name'], 
                    'last_name': old_post['last_name'],
                    'username': old_post['username'],
                    'user_email': old_post['user_email'],
                     }

        else:

            context = {'re_render':re_render}
        return render(request, 'dashboard/Users/add_user_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')

def AddUser(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Users'  in chk or request.user.is_superuser:
        if request.method == 'POST':
            re_render = False
            post_data = request.POST

            first_name = request.POST.get('first_name') or None
            print("first_name",first_name)

            if first_name is None:
                user_added_warning = 'Please enter first name!'  
                messages.warning(request, user_added_warning)
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['first_name'] = post_data['first_name']
                old_data['last_name'] = post_data['last_name']
                old_data['username'] = post_data['username'] 
                old_data['user_email'] = post_data['user_email'] 
                
                print("old data", old_data)
                request.session['_old_post'] = old_data 
                return HttpResponseRedirect('add_user_form/0')
                # return redirect(request.META.get('HTTP_REFERER'))

            last_name = request.POST.get('last_name') or None
            print('last_name',last_name)

            if last_name is None:
                user_added_warning = 'Please enter last name!'  
                messages.warning(request, user_added_warning)
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['first_name'] = post_data['first_name']
                old_data['last_name'] = post_data['last_name']
                old_data['username'] = post_data['username']
                old_data['user_email'] = post_data['user_email'] 
                
                print("old data", old_data)
                request.session['_old_post'] = old_data 
                return HttpResponseRedirect('add_user_form/0')
                # return redirect(request.META.get('HTTP_REFERER'))

            username = request.POST.get('username') or None
            print('username',username)

            if username is None:
                user_added_warning = 'Please enter username!'  
                messages.warning(request, user_added_warning)
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['first_name'] = post_data['first_name']
                old_data['last_name'] = post_data['last_name']
                old_data['username'] = post_data['username']
                old_data['user_email'] = post_data['user_email']
                
                print("old data", old_data)
                request.session['_old_post'] = old_data 
                return HttpResponseRedirect('add_user_form/0')
                # return redirect(request.META.get('HTTP_REFERER'))
            

            user_email = request.POST.get('user_email') or None
            print('user_email',user_email)

            if user_email is None:
                user_added_warning = 'Please enter email!'  
                messages.warning(request, user_added_warning)
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['first_name'] = post_data['first_name']
                old_data['last_name'] = post_data['last_name']
                old_data['username'] = post_data['username'] 
                old_data['user_email'] = post_data['user_email']
                
                print("old data", old_data)
                request.session['_old_post'] = old_data 
                return HttpResponseRedirect('add_user_form/0')
                # return redirect(request.META.get('HTTP_REFERER'))
            

            password = request.POST.get('password') or None
            print('password',password)

            if password is None:
                user_added_warning = 'Please enter password!'  
                messages.warning(request, user_added_warning)
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['first_name'] = post_data['first_name']
                old_data['last_name'] = post_data['last_name']
                old_data['username'] = post_data['username']
                old_data['user_email'] = post_data['user_email']
                
                print("old data", old_data)
                request.session['_old_post'] = old_data 
                return HttpResponseRedirect('add_user_form/0')
                # return redirect(request.META.get('HTTP_REFERER'))

            confirm_password = request.POST.get('confirm_password') or None
            print('confirm_password',confirm_password)


            if confirm_password is None:
                user_added_warning = 'Please enter confrim password!'  
                messages.warning(request, user_added_warning)
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['first_name'] = post_data['first_name']
                old_data['last_name'] = post_data['last_name']
                old_data['username'] = post_data['username']
                old_data['user_email'] = post_data['user_email']
                
                print("old data", old_data)
                request.session['_old_post'] = old_data 
                return HttpResponseRedirect('add_user_form/0')
                # return redirect(request.META.get('HTTP_REFERER'))



            if password != confirm_password:
                user_added_warning = 'Password not matched!'  
                messages.warning(request, user_added_warning)
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['first_name'] = post_data['first_name']
                old_data['last_name'] = post_data['last_name']
                old_data['username'] = post_data['username']
                old_data['user_email'] = post_data['user_email']
                
                print("old data", old_data)
                request.session['_old_post'] = old_data 
                return HttpResponseRedirect('add_user_form/0')
                # return redirect(request.META.get('HTTP_REFERER'))

            if User.objects.filter(username=username).exists():

                user_added_warning = 'Username already exists!'  
                messages.warning(request, user_added_warning)
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['first_name'] = post_data['first_name']
                old_data['last_name'] = post_data['last_name']
                old_data['username'] = post_data['username']
                old_data['user_email'] = post_data['user_email']
                
                print("old data", old_data)
                request.session['_old_post'] = old_data 
                return HttpResponseRedirect('add_user_form/0')
                # return redirect(request.META.get('HTTP_REFERER'))


            user_instance = User.objects.create_user(username=username, email=user_email, password=password, first_name=first_name, last_name=last_name,is_staff=1)

            user_instance.save()
            
            user_added_success = 'User' + ' ' + user_instance.username + ' ' + 'added successfully !'  
            messages.success(request, user_added_success)
            if '_old_post' in  request.session:
                del request.session['_old_post']    
            request.session['_old_post'] = None
            return HttpResponseRedirect('add_user_form/1')
            
    else:
        return render(request, 'dashboard/permission_denied.html')




def EditUserForm(request,id,add_button_clicked=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Users'  in chk or request.user.is_superuser:
    
        re_render = False
        user_instance = User.objects.filter(pk=id).first()
        if add_button_clicked:
            if '_old_post' in  request.session:
                del request.session['_old_post']    
                request.session['_old_post'] = None

        old_post = request.session.get('_old_post')
        print("data in old post is sub tile re render case ", old_post)

        if old_post is not None:

            re_render = True
            context= {'re_render':re_render,
                    'user_instance':user_instance, 
                    'first_name': old_post['first_name'], 
                    'last_name': old_post['last_name'],
                    'username': old_post['username'],
                    'user_email': old_post['user_email'],
                     }
        else:
            context= {'re_render':re_render,'user_instance':user_instance}

        return render(request, 'dashboard/Users/edit_user_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')

def EditUser(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Users'  in chk or request.user.is_superuser:
        if request.method == 'POST':

            re_render = False
            post_data = request.POST

            update_user_pk = request.POST.get('update_user_pk') or None
            print("update_user_pk",update_user_pk)


            first_name = request.POST.get('first_name') or None
            print("first_name",first_name)

            if first_name is None:
                user_added_warning = 'Please enter first name!'  
                messages.warning(request, user_added_warning)
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['first_name'] = post_data['first_name']
                old_data['last_name'] = post_data['last_name']
                old_data['username'] = post_data['username']
                old_data['user_email'] = post_data['user_email']
                
                print("old data", old_data)
                request.session['_old_post'] = old_data 
                add_button_clicked = 0
                url = f'edit_user_form/{update_user_pk}/{add_button_clicked}'

                return HttpResponseRedirect(url)
                # return redirect(request.META.get('HTTP_REFERER'))
            

            last_name = request.POST.get('last_name') or None
            print('last_name',last_name)

            if last_name is None:
                user_added_warning = 'Please enter last name!'  
                messages.warning(request, user_added_warning)
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['first_name'] = post_data['first_name']
                old_data['last_name'] = post_data['last_name']
                old_data['username'] = post_data['username']
                old_data['user_email'] = post_data['user_email']
                
                print("old data", old_data)
                request.session['_old_post'] = old_data 
                add_button_clicked = 0
                url = f'edit_user_form/{update_user_pk}/{add_button_clicked}'

                return HttpResponseRedirect(url)
                # return redirect(request.META.get('HTTP_REFERER'))

            username = request.POST.get('username') or None
            print('username',username)

        

            user_email = request.POST.get('user_email') or None
            print('user_email',user_email)

            if user_email is None:
                user_added_warning = 'Please enter email!'  
                messages.warning(request, user_added_warning)
                if '_old_post' in  request.session:
                        del request.session['_old_post']
                old_data = {}
                old_data['first_name'] = post_data['first_name']
                old_data['last_name'] = post_data['last_name']
                old_data['username'] = post_data['username']
                old_data['user_email'] = post_data['user_email']
                
                print("old data", old_data)
                request.session['_old_post'] = old_data 
                add_button_clicked = 0
                url = f'edit_user_form/{update_user_pk}/{add_button_clicked}'

                return HttpResponseRedirect(url)
                # return redirect(request.META.get('HTTP_REFERER'))

            password = request.POST.get('password') or None
            print('password',password)
        
            if password:

                confirm_password = request.POST.get('confirm_password') or None
                print('confirm_password',confirm_password)


                if confirm_password is None:
                    user_added_warning = 'Please enter confrim password!'  
                    messages.warning(request, user_added_warning)
                    if '_old_post' in  request.session:
                        del request.session['_old_post']
                    old_data = {}
                    old_data['first_name'] = post_data['first_name']
                    old_data['last_name'] = post_data['last_name']
                    old_data['username'] = post_data['username']
                    old_data['user_email'] = post_data['user_email']
                    
                    print("old data", old_data)
                    request.session['_old_post'] = old_data 
                    add_button_clicked = 0
                    url = f'edit_user_form/{update_user_pk}/{add_button_clicked}'

                    return HttpResponseRedirect(url)
                    # return redirect(request.META.get('HTTP_REFERER'))
                

                if password != confirm_password:
                    user_added_warning = 'Password not matched!'  
                    messages.warning(request, user_added_warning)
                    if '_old_post' in  request.session:
                        del request.session['_old_post']
                    old_data = {}
                    old_data['first_name'] = post_data['first_name']
                    old_data['last_name'] = post_data['last_name']
                    old_data['username'] = post_data['username']
                    old_data['user_email'] = post_data['user_email']
                    
                    print("old data", old_data)
                    request.session['_old_post'] = old_data 
                    add_button_clicked = 0
                    url = f'edit_user_form/{update_user_pk}/{add_button_clicked}'

                    return HttpResponseRedirect(url)
                    # return redirect(request.META.get('HTTP_REFERER')) 
    
            else:
                pass
            
            
            

            user_instance = User.objects.filter(pk=update_user_pk).first()

            if username is None:
                user_added_warning = 'Empty username not allowed!'  
                messages.warning(request, user_added_warning)
                if '_old_post' in  request.session:
                    del request.session['_old_post']
                old_data = {}
                old_data['first_name'] = post_data['first_name']
                old_data['last_name'] = post_data['last_name']
                old_data['username'] = post_data['username']
                old_data['user_email'] = post_data['user_email']
                
                print("old data", old_data)
                request.session['_old_post'] = old_data 
                add_button_clicked = 0
                url = f'edit_user_form/{update_user_pk}/{add_button_clicked}'

                return HttpResponseRedirect(url)
                

            elif username != user_instance.username:
                    if User.objects.filter(username=username).exists():

                        user_added_warning = 'Username already exists!'  
                        messages.warning(request, user_added_warning)
                        if '_old_post' in  request.session:
                            del request.session['_old_post']
                        old_data = {}
                        old_data['first_name'] = post_data['first_name']
                        old_data['last_name'] = post_data['last_name']
                        old_data['username'] = post_data['username']
                        old_data['user_email'] = post_data['user_email']
                        
                        print("old data", old_data)
                        request.session['_old_post'] = old_data 
                        add_button_clicked = 0
                        url = f'edit_user_form/{update_user_pk}/{add_button_clicked}'

                        return HttpResponseRedirect(url)
    
            else:
                 pass
                





            user_instance.first_name = first_name
            user_instance.last_name = last_name
            user_instance.username = username
            user_instance.email = user_email


            if password:
                user_instance.set_password(password)
                print("password updated succesfully")
            else:
                pass

            user_instance.save()

            user_added_success = 'User' + ' ' + user_instance.username + ' ' + 'updated successfully !'  
            messages.success(request, user_added_success)
            
            add_button_clicked = 0
            url = f'edit_user_form/{update_user_pk}/{add_button_clicked}'

            return HttpResponseRedirect(url)
    else:
        return render(request, 'dashboard/permission_denied.html')    
    





