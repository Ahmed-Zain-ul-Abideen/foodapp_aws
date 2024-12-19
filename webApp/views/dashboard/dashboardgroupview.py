from django.shortcuts import render,redirect, HttpResponseRedirect
from webApp.models import *
from django.contrib import messages
from django.core.paginator import Paginator
from geopy.geocoders import Nominatim
from django.http import JsonResponse
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth import logout
from webApp.templatetags.webApp_extras import user_role

def Grouplist(request):  
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Roles'  in chk or request.user.is_superuser:
     
    
        all_group = Group.objects.exists()
        if not all_group:
            ven = "Not Found"
            
        else: 
            p = Paginator(Group.objects.all().order_by('-id'),15)
            page = request.GET.get('page')
            ven = p.get_page(page) 
        context = {'ven':ven}
        return render(request, 'dashboard/Groups/index.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')

def AddGroupForm(request,add_button_clicked=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashbaord')
    
    if 'Roles'  in chk or request.user.is_superuser:
        re_render = False
        module = SystemModules.objects.all()

        print("add_button_clicked", add_button_clicked)
        if add_button_clicked:
            if '_old_post' in request.session:
                del request.session['_old_post']
            request.session['_old_post'] = None
        
        old_post = request.session.get('_old_post')
        print("data in old post is sub tile re render case ", old_post)

        if old_post is not None:
            re_render = True

            selcted_modules = old_post['selcted_modules']
            print("selcted_modules",selcted_modules)
            if selcted_modules:
                
                selected_modules_int = [int(i) for i in old_post['selected_module_dropdown']]

                modules = SystemModules.objects.filter(id__in=selected_modules_int)
                module_names = [module.module for module in modules]
                print("module_names",module_names)



                context= {'re_render':re_render,
                        'group':group,
                        'module':module, 
                        'module_names':module_names,                    
                        'group_name': old_post['group_name'],
                        'selcted_modules' : selcted_modules
                        }
            else:
                context= {'re_render':re_render,
                        'group':group,
                        'module':module,                     
                        'group_name': old_post['group_name'], 
                        'selcted_modules' : selcted_modules
                        }
        else:
            context= {'re_render':re_render,'module':module}
        return render(request, 'dashboard/Groups/add_group_form.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')

def AddGroup(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Roles'  in chk or request.user.is_superuser:
        re_render = False
        post_data = request.POST
        selcted_modules = True

        selected_modules = request.POST.getlist('selected_module_dropdown') or None
        print("selected_modules",selected_modules)
        if selected_modules is None:
            selcted_modules = False
        else:
            if not len(selected_modules):
                selcted_modules = False


        if selected_modules is None:
            user_added_warning = 'Please select module!'  
            messages.warning(request, user_added_warning)
            if '_old_post' in request.session:
                del request.session['_old_post']
            old_data = {}
            old_data['group_name'] = post_data['group_name']  
            old_data['selected_module_dropdown'] = request.POST.getlist('selected_module_dropdown') or None   
            old_data['selcted_modules'] = selcted_modules

            print("old data", old_data)
            request.session['_old_post'] = old_data
            return HttpResponseRedirect('add_group_form/0')

        group_name = request.POST.get('group_name') or None
        print("group_name",group_name)

        if group_name is None:
            user_added_warning = 'Please enter name!'  
            messages.warning(request, user_added_warning)
            if '_old_post' in request.session:
                del request.session['_old_post']
            old_data = {}
            old_data['group_name'] = post_data['group_name']  
            old_data['selected_module_dropdown'] = request.POST.getlist('selected_module_dropdown') or None   
            old_data['selcted_modules'] = selcted_modules

            print("old data", old_data)
            request.session['_old_post'] = old_data
            return HttpResponseRedirect('add_group_form/0')
            # return redirect(request.META.get('HTTP_REFERER'))
        

        

        group_instance = Group.objects.create(name = group_name)
        group_instance.save()

        

        for module in selected_modules:
            module_instance = SystemModules.objects.filter(pk=int(module)).first()
            link_group_module_instane = LinkGroupModule.objects.create(group = group_instance.name ,module = module_instance.module )
            

        link_group_module_instane.save()


        group_added_success = 'Group' + ' ' + group_instance.name + ' ' + 'added successfully !'  
        messages.success(request, group_added_success)
        if '_old_post' in  request.session:
            del request.session['_old_post']    
        request.session['_old_post'] = None
        add_button_clicked = 0
            
        return HttpResponseRedirect('add_group_form/1')
    else:
        return render(request, 'dashboard/permission_denied.html')


def EditUserRole(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Roles'  in chk or request.user.is_superuser:

        # if not request.user.is_superuser:
        #     logout(request)
        #     return redirect('login')

        all_user = User.objects.exists()
        all_roles = Group.objects.all()
        
        
        
        superadmins = []
        admins = []
        chefs = []

        if all_user:
            users = User.objects.exclude(is_staff=False).exclude(is_superuser = True).prefetch_related('groups')
            
            for user in users:
                user_groups = list(user.groups.values_list('name', flat=True))
                if 'Superadmin' in user_groups:
                    superadmins.append(user.id)
                if 'Admin' in user_groups:
                    admins.append(user.id)
                if 'Chef' in user_groups:
                    chefs.append(user.id)

            paginator = Paginator(users.order_by('-id'), 15)
            page = request.GET.get('page')
            paginated_users = paginator.get_page(page)
            
            for user in paginated_users:
                user.groups_list = list(user.groups.values_list('name', flat=True))
            
            context = {
                'ven': paginated_users,
                'superadmins': superadmins,
                'admins': admins,
                'chefs': chefs,
                'all_roles':all_roles
            }
        else:
            context = {'ven': "Not Found"}

        return render(request, 'dashboard/Groups/edit_user_role.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')

from django.contrib.auth.models import User, Group


def EditUserRoleNotif(request):

    if request.method == 'POST':

        role_id = request.POST.get("role_id")
        print("role_id", role_id)
        user_id = request.POST.get("ven_id")
        print("user_id", user_id)
    
        user = User.objects.get(id=user_id)
        group = Group.objects.get(id=role_id) 

        if user and group:
            user.groups.clear()
            
            user.groups.add(group)
            
            user.save()
            
            data = {'status': 'success', 'message': 'Role updated successfully!'}
        else:
            data = {'status': 'error', 'message': 'User or Group not found'}
        
        return JsonResponse(data)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# def EditUserRoleNotif(request):
    
    
#     user_id = request.GET.get("role_id")
#     print("user_id", user_id)
#     notif_field = request.GET.get("ven_id")
#     print("group_id", notif_field)
    
    
#     user_instance = User.objects.get(id=user_id)
    
    
#     def remove_all_groups_except(group_to_keep):
#         groups_to_remove = user_instance.groups.exclude(name=group_to_keep.name)
#         user_instance.groups.remove(*groups_to_remove)
    
#     if notif_field == 'superadmin_status':
#         new_group = Group.objects.get(name='Superadmin')

#         if new_group in user_instance.groups.all():
#             user_instance.groups.remove(new_group)
#             user_instance.is_superuser = False
#             resp_message = 'Super Admin access revoked'
        
#         else:
#             remove_all_groups_except(new_group)
#             user_instance.is_superuser = True
#             user_instance.groups.add(new_group)

#             resp_message = 'Super Admin access granted'

#     elif notif_field == 'admin_status':
#         new_group = Group.objects.get(name='Admin')
#         if new_group in user_instance.groups.all():
#             user_instance.groups.remove(new_group)
#             user_instance.is_staff = False
#             resp_message = 'Admin access revoked'
        
#         else:
#             remove_all_groups_except(new_group)
#             user_instance.is_staff = True
#             user_instance.groups.add(new_group)
#             resp_message = 'Admin access granted'

#     elif notif_field == 'chef_status':
#         new_group = Group.objects.get(name='Chef')
#         if new_group in user_instance.groups.all():
#             user_instance.groups.remove(new_group)
#             resp_message = 'Chef access revoked'
#         else:

#             remove_all_groups_except(new_group)
#             user_instance.groups.add(new_group)
#             resp_message = 'Chef access granted'

#     else:
#         return JsonResponse({'resp_message': 'Invalid notification field'}, status=400)
        
    
#     user_instance.save()

#     data = {'resp_message': resp_message}
#     return JsonResponse(data)



def EditRolePermissions(request,id,add_button_clicked=None):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Roles'  in chk or request.user.is_superuser:

        group = Group.objects.filter(id = id).first()
        group_name = group.name

        # list of modules associated with selected Group from the table LinkGroupModule 
        modules_list = LinkGroupModule.objects.filter(group=group_name).values_list('module', flat=True)
        print("modules_list",modules_list)

        module = SystemModules.objects.all()
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
            selcted_modules = old_post['selcted_modules']
            print("selcted_modules",selcted_modules)
            if selcted_modules:
                
                selected_modules_int = [int(i) for i in old_post['selected_module_dropdown']]

                modules = SystemModules.objects.filter(id__in=selected_modules_int)
                module_names = [module.module for module in modules]
                print("module_names",module_names)



                context= {'re_render':re_render,
                        'group':group,
                        'module':module, 
                        'module_names':module_names,
                        'user_instance':user_instance, 
                        'role_title': old_post['role_title'],
                        'selcted_modules' : selcted_modules
                        }
            else:
                context= {'re_render':re_render,
                        'group':group,
                        'module':module, 
                        'user_instance':user_instance, 
                        'role_title': old_post['role_title'], 
                        'selcted_modules' : selcted_modules
                        }
        else:
            context= {'re_render':re_render,'group':group, 'module':module, 'modules_list':modules_list}

        return render(request, 'dashboard/Groups/edit_role_permission.html', context)
    else:
        return render(request, 'dashboard/permission_denied.html')


def SubmitEditRolePermissions(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Roles'  in chk or request.user.is_superuser:

        if request.method == 'POST':

            re_render = False
            post_data = request.POST

            selcted_modules = True

            selected_modules = request.POST.getlist('selected_module_dropdown') or None
            print("selected_modules",selected_modules)
            if selected_modules is None:
                selcted_modules = False
            else:
                if not len(selected_modules):
                    selcted_modules = False

            if selected_modules is None:
                user_added_warning = 'Please select module!'  
                messages.warning(request, user_added_warning)
                if '_old_post' in request.session:
                    del request.session['_old_post']
                old_data = {}
                old_data['role_title'] = post_data['role_title']  
                old_data['selected_module_dropdown'] = request.POST.getlist('selected_module_dropdown') or None   
                old_data['selcted_modules'] = selcted_modules

                print("old data", old_data)
                request.session['_old_post'] = old_data

                add_button_clicked = 0
                url = f'edit_role_permissions/{update_role_pk}/{add_button_clicked}'

                return HttpResponseRedirect(url)
            


            update_role_pk = request.POST.get('update_role_pk') or None
            print("update_role_pk",update_role_pk)

            role_title = request.POST.get('role_title') or None
            print("role_title", role_title )
            
            if role_title is None:
                user_added_warning = 'Please enter name!'  
                messages.warning(request, user_added_warning)
                if '_old_post' in request.session:
                    del request.session['_old_post']
                old_data = {}
                old_data['role_title'] = post_data['role_title']  
                old_data['selected_module_dropdown'] = request.POST.getlist('selected_module_dropdown') or None   
                old_data['selcted_modules'] = selcted_modules

                print("old data", old_data)
                request.session['_old_post'] = old_data

                add_button_clicked = 0
                url = f'edit_role_permissions/{update_role_pk}/{add_button_clicked}'

                return HttpResponseRedirect(url)

            if role_title:
                group_instance = Group.objects.filter(id = update_role_pk ).first()
                group_instance.name = role_title
                group_instance.save()
            else:
                pass


            


            

            

            group = Group.objects.filter(id = update_role_pk).first()
            print("group",group)

            

            LinkGroupModule.objects.filter(group=group.name).delete()

            for module in selected_modules:
                module_instance = SystemModules.objects.filter(pk=int(module)).first()
                link_group_module_instane = LinkGroupModule.objects.create(group = group.name ,module = module_instance.module )
                

            link_group_module_instane.save()

            

            link_group_module_instane_added_success =  group.name + ' role permissions updated successfully!'  
            messages.success(request, link_group_module_instane_added_success)
            if '_old_post' in  request.session:
                del request.session['_old_post']    
            request.session['_old_post'] = None
            add_button_clicked = 0
            url = f'edit_role_permissions/{update_role_pk}/{add_button_clicked}'

            return HttpResponseRedirect(url)
            # return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'dashboard/permission_denied.html')
    





def DeleteGroup(request):
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Roles'  in chk or request.user.is_superuser:
    
        print("here for deleteing role record")
        role_id = request.GET.get("role_id")    
        print("role_id", role_id)
        role_instance = Group.objects.filter(id=role_id).first()
        role_name = role_instance.name.title()

        role_instance.delete() 
        print("record deleted Successfully!")
        data = {'role_name':role_name}
        return JsonResponse(data)
    else:
        return render(request, 'dashboard/permission_denied.html')
    

# Search roles
def  RolesCustomSearch(request): 
    group = Group.objects.filter(id = request.user.id).first()
    chk = user_role(request.user)
    print('group', group)


    print(chk)
    if len(chk) == 0:
        return redirect('login-dashboard')
    
    if 'Roles'  in chk or request.user.is_superuser:
        print("here in role custom search")
        role = request.GET.get('role') or None   
        print("role", role)
        searched_role_exist = Group.objects.filter(name__icontains=role).exists()
        if searched_role_exist:    
            searched_role = list(Group.objects.filter(name__icontains=role).values()) 
            print("list of roles",searched_role) 
            
            context = {'ven':  searched_role}  
            return JsonResponse({"success": True,"response":context}) 
        else:  
            return JsonResponse({"success": False})
    else:
        return render(request, 'dashboard/permission_denied.html')



    



