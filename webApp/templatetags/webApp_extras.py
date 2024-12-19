
from django.contrib.auth.models import User, Group
from django import template
from webApp.models import *
register = template.Library() 

def user_role(user):

    # Ensure we have a User instance
    if not isinstance(user, User):
        return []


    user_groups = user.groups.all()
    print("user_groups",user_groups)
    user_roles = []
    modules_list =[]

    all_roles = Group.objects.all()
    print("all_roles",all_roles)
    # make list of all roles 

    for role in all_roles:

        if user_groups.filter(name= role.name).exists():

            group_name = role.name
            user_roles.append(group_name)
            
            modules_list = list(LinkGroupModule.objects.filter(group=group_name).values_list('module', flat=True))

        elif user.is_superuser:
            group_name = 'Superadmin'
            user_roles.append(group_name)
        else:
            pass

    # if user_groups.filter(name='Superadmin').exists():
    #     user_roles.append('Superadmin')
    #     group_name = 'Superadmin'
    #     modules_list = list(LinkGroupModule.objects.filter(group=group_name).values_list('module', flat=True))


    # if user_groups.filter(name='Admin').exists():
    #     user_roles.append('Admin')
    #     group_name = 'Admin'
    #     modules_list = list(LinkGroupModule.objects.filter(group=group_name).values_list('module', flat=True))

        

    # if user_groups.filter(name='Chef').exists():
    #     user_roles.append('Chef')
    #     group_name = 'Chef'
    #     modules_list = list(LinkGroupModule.objects.filter(group=group_name).values_list('module', flat=True))

    
    response_data = [user.id] + user_roles

    print("response_data", response_data, type(response_data))

    response_data = response_data + modules_list

    print("response_data 2", response_data, type(response_data))

    

    
    return response_data


@register.simple_tag(takes_context=True)
def get_role_modules(context):
    request = context['request']
    user = request.user

    return user_role(user)

    # # Ensure we have a User instance
    # if not isinstance(user, User):
    #     return []

    # user_groups = user.groups.all()
    # user_roles = []
    # modules_list =[]

    # if user_groups.filter(name='Superadmin').exists():
    #     user_roles.append('Superadmin')
    #     group_name = 'Superadmin'
    #     modules_list = list(LinkGroupModule.objects.filter(group=group_name).values_list('module', flat=True))


    # if user_groups.filter(name='Admin').exists():
    #     user_roles.append('Admin')
    #     group_name = 'Admin'
    #     modules_list = list(LinkGroupModule.objects.filter(group=group_name).values_list('module', flat=True))

        

    # if user_groups.filter(name='Chef').exists():
    #     user_roles.append('Chef')
    #     group_name = 'Chef'
    #     modules_list = list(LinkGroupModule.objects.filter(group=group_name).values_list('module', flat=True))

    
    # response_data = [user.id] + user_roles

    # print("response_data", response_data, type(response_data))

    # response_data = response_data + modules_list

    # print("response_data 2", response_data, type(response_data))

    
    # return response_data



# @register.simple_tag(takes_context=True)
# def get_item(context,dice,keyn):
#     return dice.get(keyn)